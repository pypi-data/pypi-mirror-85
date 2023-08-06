/**
 * C++ Header: StringTokenizer
 *
 * Description: 
 *
 *
 * Author: Christiane Lemke <lemkec@fh-brandenburg.de>, (C) 2005
 *
 * Inspiration and Start Code found at Al Dev's C++ Programming HOW-TO
 * http://oopweb.com/CPP/Documents/CPPHOWTO/Volume/C++Programming-HOWTO.html#toc17
 *
 * Copyright & License : See COPYING file that comes with this distribution
 */

#ifndef string_tokenizer_h
#define string_tokenizer_h

#include <string>
#include <vector>
#include "ArrayIndexOutOfBoundsException.h"

using namespace std;

class StringTokenizer {

private:
    int counter;
    vector<string> tokens;

public:

    /**
    * Constructor.
    * @param str String to be tokenized.
    * @param delimiter Delimiter to be used.
    * @param emptyTokens Determines, if empty Tokens should be included, which can f.e. occur due to two subsequent delimiters. False by default.
    */
    StringTokenizer(const string& str, const string& delimiter, bool emptyTokens=false) {

        string::size_type lastPos,pos;

        if (!emptyTokens) {
            lastPos = str.find_first_not_of(delimiter, 0);
            pos = str.find_first_of(delimiter, lastPos);

            while (string::npos != pos || string::npos != lastPos) {
                tokens.push_back(str.substr(lastPos, pos - lastPos));
                lastPos = str.find_first_not_of(delimiter, pos);
                pos = str.find_first_of(delimiter, lastPos);
            }
        } else {
            lastPos = 0;
            pos = str.find_first_of(delimiter, lastPos);

            while (string::npos != pos) {
                tokens.push_back(str.substr(lastPos, pos - lastPos));
                lastPos = pos+1;
                pos = str.find_first_of(delimiter, lastPos);
            }
            tokens.push_back(str.substr(lastPos, str.length()));
        }
        counter = 0;

    }

    /**
     * Determines if there are more Tokens available through the getNext() Function.
     * @return true if there are more tokens, false if there are none.
     */
    bool hasNext() {
        return (counter != tokens.size());
    }

    /**
     * Returns the next token.
     * @return next token String.
     */
    string getNext() {
        counter++;
        return tokens[counter-1];
    }

    /**
     * Resets internal counter to zero, so that the tokenizer can be consumed again.
     */
    void reset() {
        counter=0;
    }

    /**
     * Returns token belonging to the given index.
     * @param index of the desired token.
     * @param str string in which the token will be saved
     * @return true if token existed, false if index was out of bounds.
     */
    bool getAt(int index, string& str) {
        if (index >= tokens.size())
            return false;
        else {
            str = tokens[index];
            return true;
        }
    }

	string getAt(int index) {
        if (index >= tokens.size())
            return NULL;
        else {
            return tokens[index];
        }
    }

    /**
     * Overloaded Operator [].
     * @throws ArrayIndexOutOfBounds Exception
	 */
    string operator[](int i) {
        if (i>=tokens.size())
            throw exc::ArrayIndexOutOfBoundsException();
        return tokens[i];
    }

    /**
     * Determines number of Tokens.
     * @return number of tokens
     */
    int size() {
        return tokens.size();
    }
};

#endif

