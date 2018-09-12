import nltk
import collections

from boolean import BooleanModel

# Build from sources: https://github.com/laurentluce/python-algorithms
from algorithms.binary_tree import Node

class IRSystem():

    def __init__(self, docs=None, stop_words=[]):
        if docs is None:
            raise UserWarning('Docs should not be none')
        self._docs = docs
        self._stemmer = nltk.stem.porter.PorterStemmer()
        self._inverted_index = self._preprocess_corpus(stop_words)
        self._print_inverted_index()

    def _preprocess_corpus(self, stop_words):
        index = {}
        for i, doc in enumerate(self._docs):
            for word in doc.split():
                if word in stop_words:
                    continue
                token = self._stemmer.stem(word.lower())
                if index.get(token, -244) == -244:
                    index[token] = Node(i + 1)
                elif isinstance(index[token], Node):
                    index[token].insert(i + 1)
                else:
                    raise UserWarning('Wrong data type for posting list')
        return index

    def _print_inverted_index(self):
        print('INVERTED INDEX:\n')
        for word, tree in self._inverted_index.items():
            print('{}: {}'.format(word, [doc_id for doc_id in tree.tree_data() if doc_id != None]))
        print()

    def _get_posting_list(self, word):
        return [doc_id for doc_id in self._inverted_index[word].tree_data() if doc_id != None]

    @staticmethod
    def _parse_query(infix_tokens):
        """ Parse Query 
        Parsing done using Shunting Yard Algorithm 
        """
        precedence = {}
        precedence['NOT'] = 3
        precedence['AND'] = 2
        precedence['OR'] = 1
        precedence['('] = 0
        precedence[')'] = 0    

        output = []
        operator_stack = []

        for token in infix_tokens:
            if (token == '('):
                operator_stack.append(token)
            
            # if right bracket, pop all operators from operator stack onto output until we hit left bracket
            elif (token == ')'):
                operator = operator_stack.pop()
                while operator != '(':
                    output.append(operator)
                    operator = operator_stack.pop()
            
            # if operator, pop operators from operator stack to queue if they are of higher precedence
            elif (token in precedence):
                # if operator stack is not empty
                if (operator_stack):
                    current_operator = operator_stack[-1]
                    while (operator_stack and precedence[current_operator] > precedence[token]):
                        output.append(operator_stack.pop())
                        if (operator_stack):
                            current_operator = operator_stack[-1]
                operator_stack.append(token) # add token to stack
            else:
                output.append(token.lower())

        # while there are still operators on the stack, pop them into the queue
        while (operator_stack):
            output.append(operator_stack.pop())

        return output

    def process_query(self, query):
        # prepare query list
        query = query.replace('(', '( ')
        query = query.replace(')', ' )')
        query = query.split(' ')

        indexed_docIDs = list(range(1, len(self._docs) + 1))

        results_stack = []
        postfix_queue = collections.deque(self._parse_query(query)) # get query in postfix notation as a queue

        while postfix_queue:
            token = postfix_queue.popleft()
            result = [] # the evaluated result at each stage
            # if operand, add postings list for term to results stack
            if (token != 'AND' and token != 'OR' and token != 'NOT'):
                token = self._stemmer.stem(token) # stem the token
                # default empty list if not in dictionary
                if (token in self._inverted_index):
                    result = self._get_posting_list(token)
            
            elif (token == 'AND'):
                right_operand = results_stack.pop()
                left_operand = results_stack.pop()
                result = BooleanModel.and_operation(left_operand, right_operand)   # evaluate AND

            elif (token == 'OR'):
                right_operand = results_stack.pop()
                left_operand = results_stack.pop()
                result = BooleanModel.or_operation(left_operand, right_operand)    # evaluate OR

            elif (token == 'NOT'):
                right_operand = results_stack.pop()
                result = BooleanModel.not_operation(right_operand, indexed_docIDs) # evaluate NOT

            results_stack.append(result)                        

        # NOTE: at this point results_stack should only have one item and it is the final result
        if len(results_stack) != 1: 
            print("ERROR: Invalid Query. Please check query syntax.") # check for errors
            return None
        
        return results_stack.pop()