/* 
 * File:   Methods.h
 * Author: qij
 * Program Date:   2010.11.05
 * Modifier:       QI Ji <qij@fudan.edu.cn>
 * Last Modified:  2010.11.05
 ***************************
 * Version: alpha 1.0
 ***************************
 */

#include <string>

#include "StringTokenizer.h"
#include "tree.h"

using namespace std;

//get size of a file
unsigned long get_file_size(const char *filename) {
    struct stat buf;
    if(stat(filename, &buf)<0)
    {
        return 0;
    }
    return (unsigned long)buf.st_size;
}

//if a string starts with a suffix
bool startWith(string& refer, string sub) {
    if(refer.length()<sub.length()) return false;
    if(refer.substr(0,sub.length())==sub) return true;
    return false;
}

//if a string ends with a suffix
bool endWith(string& refer, string sub) {
    if(refer.length()<sub.length()) return false;
    if(refer.substr(refer.length()-sub.length(),sub.length())==sub) return true;
    return false;
}

//trim a string (space or tab)
void trim(string& str) {
    //trim right
    str.erase(str.find_last_not_of(' ')+1);
    str.erase(str.find_last_not_of('\t')+1);
    //trim left
    str.erase(0,str.find_first_not_of(' '));
    str.erase(0,str.find_first_not_of('\t'));
}

//replace pattern within a string
void stringReplace(string& s_src, string s_old, string s_new) {
    string::size_type pos=0;
    string::size_type len_old=s_old.size();
    string::size_type len_new=s_new.size();
    
    while((pos=s_src.find(s_old,pos)) != string::npos) {
        s_src.replace(pos, len_old, s_new);
        pos += len_new;
    }
}

//if a file is a folder
bool isDir(string filename) {
    DIR* pdir;
    if ((pdir = opendir(filename.c_str())) == NULL) {
        return false;
    }
    closedir(pdir);
    return true;
}

//go through a folder, save all filenames to a vector
void pathTraversal(vector<string>& vec, string& path, string& suffix) {
    DIR* pdir;
    struct dirent* pent;
    string child_path;    
    //open directory
    if ((pdir = opendir(path.c_str())) == NULL) {
        if(endWith(path, suffix)) vec.push_back(path);
        return;
    }
    //read directory
    while ((pent = readdir(pdir)) != NULL) {
        string filename = pent->d_name;
        if ((filename == ".") || (filename == "..")) continue;

        child_path = path + "/" + filename;
        pathTraversal(vec, child_path,suffix);
    }
    closedir(pdir);
}

//remove a folder
void removeDir(string path) {
    DIR* pdir;
    struct dirent* pent;
    string child_path;

    //open directory
    if ((pdir = opendir(path.c_str())) == NULL) {
        remove(path.c_str());
        return;
    }
    //read directory
    while ((pent = readdir(pdir)) != NULL) {
        string filename = pent->d_name;
        if ((filename == ".") || (filename == "..")) continue;

        child_path = path + "/" + filename;
        removeDir(child_path);
    }
    closedir(pdir);
    remove(path.c_str());
}

long binarySearchInt(vector<int> vec, int site) {
    if (vec.size() == 0) return -1;
    long low = 0;
    long high = vec.size() - 1;

    long mid=-1;
    long current=0;
    while (low <= high) {
        mid = (low + high) / 2;
        current = vec[mid];

        if (site < current) {
            high = mid - 1;
        } else if (site > current) {
            low = mid + 1;
        } else return mid;
    }
    if(site > current) mid++;
    return mid;
}

long binarySearchDouble(vector<double> vec, double site) {
    if (vec.size() == 0) return -1;
    long low = 0;
    long high = vec.size() - 1;

    long mid=-1;
    double current=0;
    while (low <= high) {
        mid = (low + high) / 2;
        current = vec[mid];

        if (site < current) {
            high = mid - 1;
        } else if (site > current) {
            low = mid + 1;
        } else return mid;              
    }
    if(site > current) mid++;
    return mid;
}

//sort key-array
void quickSortLong(vector<long>& keys, long first, long last, bool increase) {
    long low = first;
    long high = last;
    if (first >= last) {
        return;
    }
    long mid = keys[(first + last) / 2];
    do {
        if (increase) {
            while (keys[low] < mid) {
                low++;
            }
            while (keys[high] > mid) {
                high--;
            }
        } else {
            while (keys[low] > mid) {
                low++;
            }
            while (keys[high] < mid) {
                high--;
            }
        }
        if (low <= high) {
            long temp_key = keys[low];
            keys[low] = keys[high];
            keys[high] = temp_key;

            low++;
            high--;
        }
    } while (low <= high);

    quickSortLong(keys, first, high, increase);
    quickSortLong(keys, low, last, increase);
}

//sort key-array
void quickSortDouble(vector<double>& keys, long first, long last, bool increase) {
    long low = first;
    long high = last;
    if (first >= last) {
        return;
    }
    double mid = keys[(first + last) / 2];
    do {
        if (increase) {
            while (keys[low] < mid) {
                low++;
            }
            while (keys[high] > mid) {
                high--;
            }
        } else {
            while (keys[low] > mid) {
                low++;
            }
            while (keys[high] < mid) {
                high--;
            }
        }
        if (low <= high) {
            double temp_key = keys[low];
            keys[low] = keys[high];
            keys[high] = temp_key;

            low++;
            high--;
        }
    } while (low <= high);

    quickSortDouble(keys, first, high, increase);
    quickSortDouble(keys, low, last, increase);
}

//sort value-array according to key-array
void quickSortDouble(double* keys, long* values, long first, long last, bool increase) {
    long low = first;
    long high = last;
    if (first >= last) {
        return;
    }
    double mid = keys[(first + last) / 2];
    do {
        if (increase) {
            while (keys[low] < mid) {
                low++;
            }
            while (keys[high] > mid) {
                high--;
            }
        } else {
            while (keys[low] > mid) {
                low++;
            }
            while (keys[high] < mid) {
                high--;
            }
        }
        if (low <= high) {
            double temp_key = keys[low];
            long temp_value = values[low];

            keys[low] = keys[high];
            values[low] = values[high];

            keys[high] = temp_key;
            values[high] = temp_value;

            low++;
            high--;
        }
    } while (low <= high);

    quickSortDouble(keys, values, first, high, increase);
    quickSortDouble(keys, values, low, last, increase);
}

double quantile(vector<double>& values, double percent) {
    double quant=-1;
    if(values.size()==0 || percent<0 || percent>1) return quant;
    if(values.size()==1) return values[0];

    double current=percent*(values.size()-1);
    long index=(long) current;
    if(current-index<0.001) quant=values[index];
    else if(index+1-current<0.001) quant=values[index+1];
    else {
        double ratio=current-index;
        quant=values[index]+(values[index+1]-values[index])*ratio;
    }
    return quant;
}

//if a string is numeric
bool isNumeric(string str) {
    for (long i = 0; i < str.length(); i++) {
        if((str[i]<'0' || str[i]>'9') && str[i]!='.' && str[i]!='-') return false;
    }
    return true;
}

//float abs(float value){
//    if(value<0) return -1*value;
//    return value;
//}

//double abs(double value){
//    if(value<0) return -1*value;
//    return value;
//}

long getDigit(long value) {
    long digit=1;
    while(value>=10) {
        value/=10;
        digit++;
    }
    return digit;
}

//append contents of a file to another one
void appendFile(string in_name, string out_name) {
    fprintf(stderr, "save: %s -> %s\n", in_name.c_str(),out_name.c_str());
    ofstream os;
    os.open(out_name.c_str(), ios::out|ios::app);
    if (!os) {
        fprintf(stderr, "Can NOT open file for output: %s\n", out_name.c_str());
        return;
    }

    ifstream is;
    is.open(in_name.c_str(), ios::in);
    if (is.fail()) {
        fprintf(stderr, "error[28] (not exist): %s\n", in_name.c_str());
        is.close();
        return;
    }
    string line = "";
    while (getline(is, line, '\n')) {
        os << line << "\n";
    }
    is.close();
    os.close();
}

//merge multiple files into one
void mergeFiles(vector<string>& in_names, string out_name) {
    ofstream os;
    os.open(out_name.c_str(), ios::out);
    if(!os) {
        fprintf(stderr, "Can NOT open file for output: %s\n", out_name.c_str());
        return;
    }

    for(long i=0;i<in_names.size();i++) {
        ifstream is;
        is.open(in_names[i].c_str(), ios::in);
        if (is.fail()) {
            fprintf(stderr, "error[29] (not exist): %s\n", in_names[i].c_str());
            is.close();
            return;
        }
        string line = "";
        while (getline(is, line, '\n')) {
            os<<line<<"\n";
        }
        is.close();
    }
    os.close();
}

//load values into a array from a input file
void appendArray(string in_name, unsigned long* array) {
    ifstream is;
    is.open(in_name.c_str(), ios::in);
    if (is.fail()) {
        fprintf(stderr, "error[14] (not exist): %s\n", in_name.c_str());
        is.close();
        return;
    }
    string line = "";
    long index=0;
    unsigned long value=0;
    while (getline(is, line, '\n')) {
        if(line.length()==0) continue;
        StringTokenizer nizer(line, " \t");
        if(nizer.size()<2) {
            fprintf(stderr,"error[15] (wrong token number): %s",line.c_str());
            continue;
        }
        sscanf(nizer.getAt(0).c_str(),"%ld",&index);
        sscanf(nizer.getAt(1).c_str(),"%ld",&value);
        array[index]+=value;
    }
    is.close();
}

double getPhredScore(double* scores, double number, double top_count,double ZERO) {
    double total=0;
    double score=0;

    for(long i=0;i<number;i++) {
        double temp=pow(10,scores[i]);
        cout<<i<<"\t"<<scores[i]<<"\t"<<temp<<endl;
        if(scores[i]<scores[0]*2) break;    //use *2 here because scores are minus
        if(i<top_count) score+=temp;
        total+=temp;
    }
    if(total==0) return 0;
    if(total-score<ZERO) return 100;

    score/=total;
    score=-10*log10(1-score);
    if(score>100) score=100;
    
    return score;
}

double logFactorial(long n) {
    double value=0;
    for(long i=0;i<n;i++) value+=log10(i+1);
    return value;
}

//double fisherTest(long a,long b,long c,long d) {
//    double value=0;
//    bool diagonal=true;
//    long start=min(min(a,b),min(c,d));
//
//    if(start==a || start==d) diagonal=true;
//    else diagonal=false;
//
//    double factor=logFactorial(a+b)+logFactorial(c+d)+logFactorial(a+c)+logFactorial(b+d)-logFactorial(a+b+c+d);
//
//    for(long i=start;i>=0;i--) {
//        double temp=factor-logFactorial(a)-logFactorial(b)-logFactorial(c)-logFactorial(d);
//        temp=pow(10,temp);
////        cout<<i<<": "<<temp<<endl;
//        value+=temp;
//        if(diagonal) {
//            a--;
//            b++;
//            c++;
//            d--;
//        } else {
//            a++;
//            b--;
//            c--;
//            d++;
//        }
//    }
//    return value;
//}

double fisherTest(long a,long b,long c,long d,bool single_side) {
    double value=0;
    bool diagonal=true;
    long start=min(min(a,b),min(c,d));
    long end=min(min(a+b,c+d),min(a+c,b+d));

    double factor=logFactorial(a+b)+logFactorial(c+d)+logFactorial(a+c)+logFactorial(b+d)-logFactorial(a+b+c+d);
    double ori_value=factor-logFactorial(a)-logFactorial(b)-logFactorial(c)-logFactorial(d);
    ori_value=pow(10,ori_value);

    if (start == a || start == d) {
        diagonal = true;
    } else {
        diagonal = false;
    }

    if (diagonal) {
        a-=start;
        b+=start;
        c+=start;
        d-=start;
    } else {
        a+=start;
        b-=start;
        c-=start;
        d+=start;
    }
    
    for(long i=0;i<=end;i++) {
        double temp=factor-logFactorial(a)-logFactorial(b)-logFactorial(c)-logFactorial(d);
        temp=pow(10,temp);
        if(temp<=ori_value) value+=temp;
        if(diagonal) {
            a++;
            b--;
            c--;
            d++;
        } else {
            a--;
            b++;
            c++;
            d--;            
        }
        if(single_side && i>start) break;
    }
    return value;
}

long getRandem(long max) {
    long value=(long) (1.0*rand()/RAND_MAX*max);
    if(value>max-1) value=max-1;
    if(value<0) value=0;
    return value;
}

bool getWebTime() {
    bool check=false;
    
    FILE *fstream = NULL;
    char buff[1024];
    memset(buff, 0, sizeof (buff));

    string address = "time.nist.gov";
    string cmd = "rdate -p " + address + " 2>&1";
    if ((fstream = popen(cmd.c_str(), "r")) == NULL) {
        return check;
    }

    stringstream ss;
    while (fgets(buff, sizeof (buff), fstream) != NULL) {
        ss << buff;
    }

    long index = 0;
    string line = "";
    while (getline(ss, line, '\n')) {
//        cout << index << ": " << line << endl;
        if (line.find_first_of("rdate:") != string::npos && line.find_first_of(address) != string::npos) {
            StringTokenizer nizer(line, "\t");
            if(nizer.size()==2) {
                string date=nizer.getAt(1);
                StringTokenizer nizer1(date," ");
                if(nizer1.size()==5) {
                    long year=0;
                    sscanf(nizer1.getAt(4).c_str(),"%ld",&year);
                    if(year<2020) check=true;
                }
            }            
        }
        index++;
    }
    pclose(fstream);
    
    return check;
}