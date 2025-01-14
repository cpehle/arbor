#pragma once

#include <memory>
#include <string>
#include <utility>

#include "expression.hpp"
#include "lexer.hpp"
#include "module.hpp"

class Parser : public Lexer {
public:

    explicit Parser(Module& m, bool advance=true);
    Parser(std::string const&);
    bool parse();

    expression_ptr parse_prototype(std::string);
    expression_ptr parse_statement();
    expression_ptr parse_identifier();
    expression_ptr parse_integer();
    expression_ptr parse_real();
    expression_ptr parse_call();
    expression_ptr parse_expression(int prec);
    expression_ptr parse_expression();
    expression_ptr parse_primary();
    expression_ptr parse_parenthesis_expression();
    expression_ptr parse_line_expression();
    expression_ptr parse_stoich_expression();
    expression_ptr parse_stoich_term();
    expression_ptr parse_reaction_expression();
    expression_ptr parse_conserve_expression();
    expression_ptr parse_binop(expression_ptr&&, Token);
    expression_ptr parse_unaryop();
    expression_ptr parse_local();
    expression_ptr parse_solve();
    expression_ptr parse_conductance();
    expression_ptr parse_block(bool);
    expression_ptr parse_initial();
    expression_ptr parse_if();

    symbol_ptr parse_procedure();
    symbol_ptr parse_function();

    std::string const& error_message() {
        return error_string_;
    }

    // functions for parsing descriptive blocks
    // these are called in the first pass, and do not
    // construct any AST information
    void parse_neuron_block();
    void parse_state_block();
    void parse_units_block();
    void parse_parameter_block();
    void parse_assigned_block();
    void parse_title();

private:
    Module *module_;

    std::vector<Token> comma_separated_identifiers();
    std::vector<Token> unit_description();
    std::string value_literal();
    std::pair<Token, Token> range_description();

    /// build the identifier list
    void add_variables_to_symbols();

    // helper function for logging errors
    void error(std::string msg);
    void error(std::string msg, Location loc);

    // disable default and copy assignment
    Parser();
    Parser(Parser const &);

    void parse_unit();
    bool expect(tok, const char *str="");
    bool expect(tok, std::string const& str);
};
