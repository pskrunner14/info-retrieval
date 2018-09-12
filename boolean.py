import math

class BooleanModel():
    
    @staticmethod
    def and_operation(left_operand, right_operand):
        # perform 'merge'
        result = []                                 # results list to be returned
        l_index = 0                                 # current index in left_operand
        r_index = 0                                 # current index in right_operand
        l_skip = int(math.sqrt(len(left_operand)))  # skip pointer distance for l_index
        r_skip = int(math.sqrt(len(right_operand))) # skip pointer distance for r_index

        while (l_index < len(left_operand) and r_index < len(right_operand)):
            l_item = left_operand[l_index]  # current item in left_operand
            r_item = right_operand[r_index] # current item in right_operand
            
            # case 1: if match
            if (l_item == r_item):
                result.append(l_item)   # add to results
                l_index += 1            # advance left index
                r_index += 1            # advance right index
            
            # case 2: if left item is more than right item
            elif (l_item > r_item):
                # if r_index can be skipped (if new r_index is still within range and resulting item is <= left item)
                if (r_index + r_skip < len(right_operand)) and right_operand[r_index + r_skip] <= l_item:
                    r_index += r_skip
                # else advance r_index by 1
                else:
                    r_index += 1

            # case 3: if left item is less than right item
            else:
                # if l_index can be skipped (if new l_index is still within range and resulting item is <= right item)
                if (l_index + l_skip < len(left_operand)) and left_operand[l_index + l_skip] <= r_item:
                    l_index += l_skip
                # else advance l_index by 1
                else:
                    l_index += 1

        return result

    @staticmethod
    def or_operation(left_operand, right_operand):
        result = []     # union of left and right operand
        l_index = 0     # current index in left_operand
        r_index = 0     # current index in right_operand

        # while lists have not yet been covered
        while (l_index < len(left_operand) or r_index < len(right_operand)):
            # if both list are not yet exhausted
            if (l_index < len(left_operand) and r_index < len(right_operand)):
                l_item = left_operand[l_index]  # current item in left_operand
                r_item = right_operand[r_index] # current item in right_operand
                
                # case 1: if items are equal, add either one to result and advance both pointers
                if (l_item == r_item):
                    result.append(l_item)
                    l_index += 1
                    r_index += 1

                # case 2: l_item greater than r_item, add r_item and advance r_index
                elif (l_item > r_item):
                    result.append(r_item)
                    r_index += 1

                # case 3: l_item lower than r_item, add l_item and advance l_index
                else:
                    result.append(l_item)
                    l_index += 1

            # if left_operand list is exhausted, append r_item and advance r_index
            elif (l_index >= len(left_operand)):
                r_item = right_operand[r_index]
                result.append(r_item)
                r_index += 1

            # else if right_operand list is exhausted, append l_item and advance l_index 
            else:
                l_item = left_operand[l_index]
                result.append(l_item)
                l_index += 1

        return result

    @staticmethod
    def not_operation(right_operand, indexed_docIDs):
        # complement of an empty list is list of all indexed docIDs
        if (not right_operand):
            return indexed_docIDs
        
        result = []
        r_index = 0 # index for right operand
        for item in indexed_docIDs:
            # if item do not match that in right_operand, it belongs to compliment 
            if (item != right_operand[r_index]):
                result.append(item)
            # else if item matches and r_index still can progress, advance it by 1
            elif (r_index + 1 < len(right_operand)):
                r_index += 1
        return result