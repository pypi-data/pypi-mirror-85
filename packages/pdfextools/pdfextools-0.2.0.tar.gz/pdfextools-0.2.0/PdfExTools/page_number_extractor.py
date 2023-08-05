import re
import sys
import json
import math

import fitz

"""
assumption:
(1) each page (other than the 1st page) should have a page number printed in header or footer.
(2) the page number might not start from 1, but should be in ascending order.
(3) sometimes the 1st page might have meta info about the document that often not appear in other pages.
"""

class PageNumberExtractor:

    class TextLineObj(object):
        """ class to represent a line of text in pdf """
        def __init__(self, text, bbox):
            self.text = text
            self.bbox = bbox

        def __repr__(self):
            result = { "Text": self.text, "Bbox": self.bbox }
            return json.dumps(result)

        def __cmp__(self, other):
            result = -1
            bbox1 = self.bbox
            bbox2 = other.bbox
            if bbox1[1] < bbox2[1]:
                result = -1
            elif bbox1[1] > bbox2[1]:
                result = 1
            else:
                if bbox1[0] < bbox2[0]:
                    result = -1
                elif bbox1[0] > bbox2[0]:
                    result = 1
                else:
                    result = 0
            return result

    def process(self, input_pdf):
        """
        entry method of the class
        return a dictionary of logical page number to physical ones (aka. the # printed on page).
        e.g., { 0:15, 1:16, 2:17, ..., 9:24 }
        """

        total_pages, cand_lines_by_page = self.get_candidate_lines(input_pdf)

        logical_pg_numbers = range(0, total_pages)

        pairs = self.find_page_numbers(cand_lines_by_page)

        result = self.fill_gaps(pairs, logical_pg_numbers)

        return result

    def get_candidate_lines(self, input_pdf, max_pages_to_check=20):
        """
        given the pdf, return the header/footer lines that likely contain page numbers.
        here use PyMuPdf to read pdf. Other pdf libraries can be used too.
        by default, pages_to_check = 20, don't have to check all pages to find a pattern
        """
        pdf_doc = fitz.open(input_pdf)

        total_pages = pdf_doc.pageCount

        cand_lines_by_page = []
        for pgn, page in enumerate(pdf_doc):
            if pgn >= max_pages_to_check:
                break

            pg_dict = page.getText("dict")

            lines = self.get_text_lines_in_page(pg_dict)

            cand_lines = []   # candidate lines to check for this page

            if len(lines) <=6:
                for line in lines:
                    cand_lines.append(line.text)
            elif len(lines) >= 3:
                cand_lines.append(lines[0].text)   # 1st line
                cand_lines.append(lines[1].text)   # 2nd line
                cand_lines.append(lines[2].text)   # 3rd line
                cand_lines.append(lines[-1].text)  # 1st last line
                cand_lines.append(lines[-2].text)  # 2nd last line
                cand_lines.append(lines[-3].text)  # 3rd last line

            cand_lines_by_page.append("\n".join(cand_lines))

        return total_pages, cand_lines_by_page

    def get_text_lines_in_page(self, page_dict):
        pieces = []
        for block in page_dict["blocks"]:
            if block["type"] != 0:  # 0 means it's text line, type=1 is image block
                continue
            for line in block["lines"]:
                bbox = self.get_rounded_bbox(line["bbox"])
                text_spans = []
                for span in line["spans"]:
                    if len(span["text"]) > 0:
                        text_spans.append(span["text"])
                text = " ".join(text_spans)
                pieces.append(self.TextLineObj(text, bbox))

        # order the lines in up-down then left-right order
        sorted_pieces = sorted(pieces, key=lambda x: (x.bbox[1], x.bbox[0]))

        merged_lines = self.merge_pieces_in_same_line(sorted_pieces)

        return merged_lines

    def get_rounded_bbox(self, bbox):
        new_box = [round(bbox[0]), round(bbox[1]), round(bbox[2]), round(bbox[3])]
        return new_box

    def merge_pieces_in_same_line(self, sorted_pieces):
        result = []
        if len(sorted_pieces) > 0:
            pieces_in_line = []
            i = 0
            prev_y = -1
            curr_y = -1
            while i < len(sorted_pieces):
                curr_piece = sorted_pieces[i]
                curr_y = curr_piece.bbox[1]
                if curr_y != prev_y and len(pieces_in_line) > 0:
                    # a new line
                    merged_pieces = self.merge_piece(pieces_in_line)
                    result.append(merged_pieces)
                    pieces_in_line = []

                pieces_in_line.append(curr_piece)
                prev_y = curr_y
                i += 1

            # handle the last piece
            pieces_in_line.append(curr_piece)
            merged_pieces = self.merge_piece(pieces_in_line)
            result.append(merged_pieces)
        return result

    def merge_piece(self, pieces):
        text_list = []
        bbox_list = []
        for piece in pieces:
            text_list.append(piece.text)
            bbox_list.append(piece.bbox)
        merged_text = " ".join(text_list)
        merged_bbox = self.merge_bboxes(bbox_list)
        return self.TextLineObj(merged_text, merged_bbox)

    def merge_bboxes(self, boxes):
        if len(boxes) == 0:
            return []
        elif len(boxes) == 1:
            return boxes[0]

        x1, y1, x2, y2 = boxes[0]
        for i in range(1, len(boxes)):
            x1 = min(x1, boxes[i][0])
            y1 = min(y1, boxes[i][1])
            x2 = max(x2, boxes[i][2])
            y2 = max(y2, boxes[i][3])
        return [x1, y1, x2, y2]

    def find_page_numbers(self, text_lines):
        """
        return a dictionary mapping logical page # to physical ones.
        e.g., {0: 11, 1: 12, 2: 13, 3: 14, 4: 15, 5: 16, 6: 17}
        """

        # step 1: assume each line is a line from a page
        # a page number suppose to be unique to the correspoding page
        # for a seen number, here to find which pages it appears in
        number_to_page_mapping = {}
        for pgn, line in enumerate(text_lines):
            #print(line)
            numbers = re.findall(r"\d+", line)
            if (numbers):
                # all numbers in this line
                for num_str in numbers:
                    num = int(num_str)
                    if num in number_to_page_mapping.keys():
                        number_to_page_mapping[num].add(pgn)
                    else:
                        number_to_page_mapping[num] = {pgn}

        print("\nnumber_to_page_list:")
        print(number_to_page_mapping)

        # step 2: the numbers appearing in only 1 page is likely the page number,
        # because a page number has to be unique across the pages (they should not appear more than once)
        # to allow some resilence to noices, a real page number might happen to occur more than once
        uniq_numbers = []
        for num, pg_list in number_to_page_mapping.items():
            if len(pg_list) <= 3:   
                uniq_numbers.append(num)

        # step 3: sort the "unique" numbers so that they are ordered along x-axis
        uniq_numbers.sort()

        print("uniq_numbers")
        print(uniq_numbers)

        # step 4: find all candidate intervals that are continuous and long enough
        cand_intervals = []
        i = 0
        j = 0
        n = len(uniq_numbers)
        min_len = max(3, round(len(text_lines) * 0.6))  # should cover >60% pages
        while i < n:
            j = i+1
            while j<n and uniq_numbers[j-1]+1 == uniq_numbers[j]:
                j += 1

            if (j-i) > min_len:
                cand_intervals.append((i, j))  # interval = [i, j), i inclusive, j exclusive

            i = j

        # step 5: find the interval that covers most logical page numbers
        max_i = 0
        max_j = 0
        max_pg_covered = 0
        for interval in cand_intervals:
            a, b = interval
            print(interval)
            pg_covered = set()
            for idx in range(a, b):
                num = uniq_numbers[idx]
                pg_covered = pg_covered.union(number_to_page_mapping[num])
                if len(pg_covered) > max_pg_covered:
                    max_i = a
                    max_j = b
                    max_pg_covered = len(pg_covered)

        longest_seq = uniq_numbers[max_i : max_j]

        print("longest_seq:")
        print(longest_seq)

        # step 5: turn list to dictionary
        cand_pairs = {}

        for num in longest_seq:
            pgn_set = number_to_page_mapping[num]
            if len(pgn_set)==1:
                pgn = next(iter(pgn_set))
                cand_pairs[pgn] = num

        print("cand_pairs:")
        print(cand_pairs)

        return cand_pairs

    def fill_gaps(self, cand_pairs, logical_pg_numbers):
        # go through the logical numbers, and fill the gap if any
        if len(cand_pairs) == 0:
            return []

        n = len(logical_pg_numbers)
        unfilled_pgn = -1
        result = [unfilled_pgn] * n
        for pgn in logical_pg_numbers:
            if pgn in cand_pairs.keys():
                result[pgn] = cand_pairs[pgn]

        i = 0
        j = 0
        while i < n:
            while i<n and result[i] != -1:
                i += 1
            
            j = i+1
            while j<n and result[j] == -1:
                j += 1
            
            # set pgn from page i (inclusive) to j (exclusive)
            if (i>0):
                k = i
                while k < min(j, n):
                    result[k] = result[k-1] + 1
                    k += 1
            elif (j<n):
                k = j-1
                while k >= i:
                    result[k] = result[k+1] - 1
                    k -= 1

            i = j

        return { idx : val for idx, val in enumerate(result) }

if __name__ == "__main__":
    pdf_file = sys.argv[1]
    
    print("pdf_file: " + pdf_file)

    extractor = PageNumberExtractor()
    page_numbers = extractor.process(pdf_file)

    print("\nresult:")
    print(page_numbers)
