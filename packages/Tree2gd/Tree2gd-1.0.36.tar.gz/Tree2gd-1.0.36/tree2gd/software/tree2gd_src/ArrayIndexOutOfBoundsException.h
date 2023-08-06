/**
 * C++ Header: ArrayIndexOutOfBoundsException
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

#include <string>

#ifndef exc_ArrayIndexOutOfBoundsException
#define exc_ArrayIndexOutOfBoundsException
namespace exc {
	
	/**
	* Exception to be thrown when operator[] is trying to access a non-existent object.
	*/
	class ArrayIndexOutOfBoundsException {
	
	public:
	
		/**
		* Constructor, initialises message Member Variable.
		*/
		ArrayIndexOutOfBoundsException() {
			message = "Exception: Array Index is out of Bounds.";
		}
		
		/**
		* Standard Destructor.
		*/
		~ArrayIndexOutOfBoundsException(){};
	
		/**
		* Returns short description of the exception.
		* @return std::string Description
		*/
		std::string getMessage() { return message; }
		
	private:
		std::string message;
	
	};
}

#endif

