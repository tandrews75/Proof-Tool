from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import clean_rule, get_line_nos, get_line_with_line_no, get_lines_in_subproof, \
    get_expressions, verify_line_citation, verify_line_citation, make_tree, is_name, is_var, verify_same_structure_FOL, \
    verify_var_replaces_some_name
from .rule import Rule

class ExistentialElim(Rule):

    name = "Existential Elimination"
    symbols = "∃E"

    
    def verify(self, current_line: ProofLineObj, proof: ProofObj, parser):
        """
        Verify proper implementation of the rule ∃E m, i
        (Existential Elimination)
        """
        rule = clean_rule(current_line.rule)
        response = ProofResponse()

        # Attempt to find line m
        try:
            target_line_nos = get_line_nos(rule)
            line_m = get_line_with_line_no(target_line_nos[0], proof)
            lines_i = get_lines_in_subproof(target_line_nos[1], proof)
            target_lines = [line_m, lines_i[0], lines_i[1]]

            # Verify that line citations are valid
            for line_no in target_line_nos:
                result = verify_line_citation(current_line.line_no, line_no)
                if result.is_valid == False:
                    return result

            # Search for lines m, i.1, i.x
            try:
                expressions = get_expressions(target_lines)
                root_m = make_tree(expressions[0], parser)
                root_i_1 = make_tree(expressions[1], parser)
                root_i_x = make_tree(expressions[2], parser)
                root_current = make_tree(current_line.expression, parser)

                # Verify root operand of line m is ∃
                if (root_m.value[0] != '∃'):
                    response.err_msg = "Error on line {}: The root operand of line {} should be the existential quantifier (∃)"\
                        .format(str(current_line.line_no), str(target_lines[0].line_no))
                    return response
                
                # Verify that root_m.right and root_i_1 have same stucture
                result = verify_same_structure_FOL(root_m.right, root_i_1, target_line_nos[0], (target_line_nos[1] + ".1"))
                if result.is_valid == False:
                    result.err_msg = 'Error on line {}: '.format(current_line.line_no) + result.err_msg
                    return result

                # Verify that all instances of the bound variable in root_m.right
                # are replaced by the same name in root_i_1
                var = root_m.value[1]
                result = verify_var_replaces_some_name(root_m.right, root_i_1, var, target_line_nos[0], (target_line_nos[1] + ".1"))
                if result.is_valid == False:
                    result.err_msg = 'Error on line {}: '.format(current_line.line_no) + result.err_msg
                    return result

                # Verify that root_i_x and current are equivalent
                if not root_i_x == root_current:
                    response.err_msg = "Error on line {}: The expressions on line {} and line {} should be equivalent"\
                        .format(str(current_line.line_no), str(target_lines[2].line_no), str(current_line.line_no))
                    return response

                # # Verify line m and line i_1 use the same predicate
                # if (root_m.right.value[0] != root_i_1.value[0]):
                #     response.err_msg = "Error on line {}: Lines {} and {} should refer to the same predicate"\
                #         .format(str(current_line.line_no), str(target_lines[0].line_no), str(target_lines[1].line_no))
                #     return response

                # # Verify that line m and current line have same number of predicate inputs
                # count_m = 0
                # count_curr = 0
                # for ch in root_m.right.value:
                #     if (is_var(ch) or is_name(ch)):
                #         count_m += 1
                # for ch in root_i_1.value:
                #     if (is_var(ch) or is_name(ch)):
                #         count_curr += 1

                # if count_m != count_curr:
                #     response.err_msg = "Error on line {}: The predicates on lines {} and {} do not have the same number of inputs"\
                #         .format(str(current_line.line_no), str(target_lines[0].line_no), str(target_lines[1].line_no))
                #     return response

                # # Verify that each variable reference on line m is replaced by the same name on current line
                # var = root_m.value[1]
                # index = 0
                # var_indexes = []

                # # Eliminate whitespace in the functions to avoid issues
                # func_m = root_m.right.value.replace(' ', '')
                # func_i_1 = root_i_1.value.replace(' ', '')

                # # Keep track of the locations (indexes) of the bound variable on line m
                # for ch in func_m:
                #     if ch == var:
                #         var_indexes.append(index)
                #     index += 1

                # # Get the values at these locations in the current line
                # # Make sure they all represent names
                # names = []
                # for i in var_indexes:
                #     names.append(func_i_1[i])
                
                # for ch in names:
                #     if not is_name(ch):
                #         response.err_msg = "Error on line {}: Instances of variable {} on line {} should be replaced with a name on line {}"\
                #             .format(str(current_line.line_no), var, str(target_lines[0].line_no), str(target_lines[1].line_no))
                #         return response
                
                # # Make sure they all use the same name
                # if len(names) > 1:
                #     for ch in names:
                #         if not ch == names[0]:
                #             response.err_msg = "Error on line {}: All instances of variable {} on line {} should be replaced with the same name on line {}"\
                #                 .format(str(current_line.line_no), var, str(target_lines[0].line_no), str(target_lines[1].line_no))
                #             return response

                # # Verify the expressions on line i_x and current line are equivalent
                # # Eliminate whitespace to avoid issues
                # func_i_x = expressions[2].replace(' ', '')
                # func_curr = current_line.expression.replace(' ', '')

                # if not func_i_x == func_curr:
                #     response.err_msg = "Error on line {}: The expressions on line {} and line {} should be equivalent"\
                #         .format(str(current_line.line_no), str(target_lines[2].line_no), str(current_line.line_no))
                #     return response

                response.is_valid = True
                return response

            except:
                response.err_msg = "Error on line {}: Line numbers are not specified correctly.  Existential Elimination: ∃E m"\
                    .format(str(current_line.line_no))
                return response

        except:
            response.err_msg = "Error on line {}: Rule not formatted properly.  Existential Elimination: ∃E m"\
                .format(str(current_line.line_no))
            return response