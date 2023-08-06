/*
 * File:   tree2gd.cpp
 * Author: qij
 *
 * Created on July 11, 2012, 2:48 PM
 */

#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <time.h>
#include <memory.h>
#include <map>
#include <set>
#include <vector>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <pthread.h>
#include <fcntl.h>
#include <unistd.h>
#include "StringTokenizer.h"
#include "tree.h"
#include "Methods.h"

using namespace std;

string VERSION="2.5 (2020.06.08)";

const string OPT_SPECIES="--species=";
const string OPT_BP="--bp=";
const string OPT_SPLIT="--split_tree=";
const string OPT_PRINT="--print=";
const string OPT_QUICK="--quick_file=";
const string OPT_PARSER="--parser_file=";
const string OPT_PAML="--paml=";
const string OPT_OMEGA="--omega=";
const string OPT_SUBBP="--sub_bp=";
const string OPT_GENOME="--genome=";
const string OPT_ISOFORM="--isoform=";
const string OPT_SAVETREE="--save_tree=";    //save rooted trees
const string OPT_DEEPVAR="--deepvar=";  //
const string OPT_ROOT="--root=";        //method for rooting

//const string OUTGROUP="outgroup";
//const string MIN_VAR="min_var";
//const string MIXED="mixed";

long MIN_SPECIES=2;         //minimum number of shared species between duplicated clades
long MIN_BOOTSTRAP=50;      //minimum bootstrap value for the considered clade
long MIN_SUB_CLADE_BP=0;    //minimum bootstrap value for the two sub-clades
long MAX_DEEP_VAR=1;    //minimum bootstrap value for the two sub-clades

string QUICK_FILE = "";     //quick-paranoid file
string PARSER_FILE = "";    //blast parser file
string OMEGA_FILE = "";     //ka/ks file
string GENOME_FILE = "";    //genome file, for skipping identification of isoforms
string ISOFORM_FILE = "";   //isoform file
bool SAVE_PAML = false;
bool SPLIT_TREE = false;
bool SAVE_ROOTED = true;
double MAX_KS=6.0;          //maximum ks for a GD event

string KW_MIN_TOPO_ERR="MIN_TOPO";
string KW_MAX_DUP_SCORE="MAX_DUP";
string KW_MAX_DUP_BRANCH="MAX_MIX";
string ROOT_METHOD=KW_MAX_DUP_BRANCH;

bool PRINT=false;

void usage(FILE *fp, long exit_code, char *program) {
    fprintf(fp, "\nProgram : %s\n", program);
    fprintf(fp, "\nVersion : %s\n", VERSION.c_str());
    fprintf(fp, "Contact : Ji QI [qij@fudan.edu.cn]\n");

    fprintf(fp, "Usage : \n\n%s species_tree gene_idmap gene_tree_list out_folder\n", program);
    fprintf(fp, "\nExample:\n");
    fprintf(fp, "%s species_tree.txt gene.idmap gene_tree.list output\n", program);
    fprintf(fp, "\nParameters:\n");
    fprintf(fp, "[%s] minimum number for overlapped species for duplicated clades: %ld\n",OPT_SPECIES.c_str(),MIN_SPECIES);
    fprintf(fp, "[%s] minimum bootstrap value: %ld\n",OPT_BP.c_str(),MIN_BOOTSTRAP);
    fprintf(fp, "[%s] minimum bp values for sub clades: %ld\n",OPT_SUBBP.c_str(),MIN_SUB_CLADE_BP);
    fprintf(fp, "[%s] split tree into subtrees [true/false]: %s\n",OPT_SPLIT.c_str(),SPLIT_TREE ? "true" : "false");
    fprintf(fp, "[%s] quickparanoid file, for clusters without a corresponding tree\n",OPT_QUICK.c_str());
    fprintf(fp, "[%s] blast_parser file, if a cluster doesn't have a outgroup OTU, find a new one\n",OPT_PARSER.c_str());
    fprintf(fp, "[%s] prepare pmal files for each cluster [true/false]: %s\n",OPT_PAML.c_str(),SAVE_PAML ? "true" : "false");
    fprintf(fp, "[%s] Ka/Ks/Omega file, tabular format\n",OPT_OMEGA.c_str());
    fprintf(fp, "[%s] list of genomes, which is ignored for identifying isoforms\n",OPT_GENOME.c_str());
    fprintf(fp, "[%s] table of isoforms, in which alternative transcirpts are ignored\n",OPT_ISOFORM.c_str());
    fprintf(fp, "[%s] output rooted trees [true/false]: %s\n",OPT_SAVETREE.c_str(), SAVE_ROOTED ? "true" : "false");
    fprintf(fp, "[%s] maximum variance of deepth: %ld\n",OPT_DEEPVAR.c_str(),MAX_DEEP_VAR);
    fprintf(fp, "[%s] method for rooting gene tree [%s/%s/%s]: %s\n",OPT_ROOT.c_str(),KW_MIN_TOPO_ERR.c_str(),KW_MAX_DUP_SCORE.c_str(),KW_MAX_DUP_BRANCH.c_str(),ROOT_METHOD.c_str());
    fprintf(fp, "     [%s]: reconcile only using depth-score on a topology, recommend for small datasets (10 species or less)\n",KW_MIN_TOPO_ERR.c_str());
    fprintf(fp, "     [%s]: reconcile using species-overlap-score, not recommend\n",KW_MAX_DUP_SCORE.c_str());
    fprintf(fp, "     [%s]: reconcile using mix info of species-overlap-score and branch length, recommend for large datasets\n",KW_MAX_DUP_BRANCH.c_str());

    fprintf(fp, "============================================================\n\n");

    exit(exit_code);
}

//structure of node for species/gene trees
struct PhyNode {
    string name;        //species/gene name
//    string alias;
//    string file_name;
    double dist;        //branch length
    double bootstrap;   //bp value
    long index;         //index on the gene tree
    long phy_index;     //index on the species tree
    bool is_leaf;       //if this node is a leaf
    long gd_count;      //number of GDs
    long lineage_count;    //number of lineage visited
    long tree_count;    //number of trees visited
    bool save;
};

//set default values for a node
void initializeNode(PhyNode & node) {
    node.name="NA";
//    node.alias="NA";
//    node.file_name="NA";
    node.dist=0;
    node.bootstrap=0;
    node.index=0;
    node.phy_index=0;
    node.is_leaf=false;
    node.gd_count=0;
    node.lineage_count=0;
    node.tree_count=0;
    node.save=true;
}

//copy contents of one node to another
void cloneNode(PhyNode & to, PhyNode & from) {
    to.name=from.name;
//    node.alias="NA";
//    to.file_name=from.file_name;
    to.dist=from.dist;
    to.bootstrap=from.bootstrap;
    to.index=from.index;
    to.phy_index=from.phy_index;
    to.is_leaf=from.is_leaf;
    to.gd_count=from.gd_count;
    to.lineage_count=from.lineage_count;
    to.tree_count=from.tree_count;
    to.save=from.save;
}

//structure of a gene pair within the same species
struct Pair {
    string species_id;
    string gene1;
    string gene2;
};

//structure of a GD from a single gene tree
struct GeneDuplication {
    long gd_id;             //id of the GD
    string gene_tree_id;    //id (name) of the gene tree
    tree<PhyNode>::iterator gene_tree_node;
//    string node_name;
    long phy_index;         //index on the species tree (e.g. level of this GD)
    long overlap_lca_index; //

    set<long> clade1;       //phy_index of species/nodes in clade1
    set<long> clade2;       //phy_index of species/nodes in clade2
    vector<Pair> gene_pairs;//gene pairs support this GD
    vector<long> child_gd1; //child gd in clade1
    vector<long> child_gd2; //child gd in clade2

    map<string,double> species_ks;   //median ks of all gene pairs for each species
    double ks;       //ks of this GD
//    long multiple;  //0 for simple gd, 1 for multiple gd (i.e. alpha/beta gds in Brassicaceae)
    long depth_var;         //

    double this_bp;         //bootstrap value of the node
    double child_bp1;       //bootstrap value of clade1
    double child_bp2;       //bootstrap value of clade2

    double median_clade_len1;   //median branch length of genes in clade1
    double median_clade_len2;   //median branch length of genes in clade2

    string comment;
    bool save;
};

//structure of a subtree on a gene tree (by enabling the split option), or a quick-paranoid cluster (a gene family without)
struct QPCluster {
    string tree_id;             //id of the cluster
    string tree_file;           //name of the quick-paranoid file
    tree<PhyNode> gene_tree;    //a pseudo-tree
    long top_phy_index;         //index of the LCA of included genes on the species tree
    vector<string> gene_ids;    //ids of genes
    vector<string> og_ids;      //
    long species_num;
    bool is_true_tree;
    bool save;
};

//structure of entry in a blast parser file
struct ParserLine {
    string query_id;
    string target_id;
    double bit_score;
    long query_len;
    long target_len;
    long query_longest_match;
    long target_longest_match;
    long query_total_match;
    long target_total_match;
};

//structure for recoding ka/ks/omega of a gene pair
struct Omega {
    double ka;
    double ks;
    double omega;
};

//sort the vector of "values" accoding to numbers in the array "keys"
void quickSortLong(long* keys, vector<string> & values, long first, long last, bool increase) {
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
            string temp_value = values[low];

            keys[low] = keys[high];
            values[low] = values[high];

            keys[high] = temp_key;
            values[high] = temp_value;

            low++;
            high--;
        }
    } while (low <= high);
    quickSortLong(keys, values, first, high, increase);
    quickSortLong(keys, values, low, last, increase);
}

long intersect(set<long> & set0, set<long> & set1) {
    long shared=0;
    for(set<long>::iterator i=set0.begin();i!=set0.end();i++) {
        if(set1.count(*i)>0) shared++;
    }
    return shared;
}

class Tree2GD {
public:
    Tree2GD(string t_file, string i_file, string l_file, string out_f);
    ~Tree2GD();

    void execute();
    tree<PhyNode>::iterator findRootWithMinTopoError(tree<PhyNode> & curr_tree);
    tree<PhyNode>::iterator findRootWithMaxScore(tree<PhyNode> & curr_tree);
    tree<PhyNode>::iterator findRootWithMaxScoreAndDist(tree<PhyNode> & curr_tree);
    void reRootTree(tree<PhyNode> & curr_tree, tree<PhyNode>::iterator outgroup);
    tree<PhyNode>::iterator getLCA(tree<PhyNode> & curr_tree, long min_index, long max_index);
    void evaluateTreeCenter(tree<PhyNode> & curr_tree, tree<PhyNode>::iterator curr_node, double & bias, double & var);
    double distOfLeaf2Parent(tree<PhyNode> & curr_tree, tree<PhyNode>::iterator parent_node, tree<PhyNode>::iterator leaf_node);
    void splitClusters();
    void addExtraRoot();
    void setIndex(tree<PhyNode> & curr_tree);
    void setPhyIndex(tree<PhyNode> & curr_tree);
    void setMinKaKs4GDs();
    void setMedianKaKs4GDs();
    void adjustGDsByKs1();
    void adjustGDsByKs2();
    void deleteNodes(tree<PhyNode> & curr_tree, vector<tree<PhyNode>::iterator> & nodes);

    void readGene2SpeciesMap(string in_name, map<string,string> & id_map);
    void readTreeList(string in_name, vector<QPCluster> & g_trees);
    void readNewickTree(string in_name, tree<PhyNode> & curr_tree, vector<tree<PhyNode>::iterator> & nodes, vector<tree<PhyNode>::iterator> & leaves, string prefix);
    void readQuickParanoid(string in_name, vector<QPCluster> & clusters,string prefix);
    void readOmega(string in_name, map<string, map<string,Omega> > & omega_map);
    void readBlastParser(string in_name, map<string,vector<ParserLine> > & gene2parsers);
    void readGenomeList(string in_name, set<string> & g_set);
    void readIgnoredIsoforms(string in_name, set<string> & isoform_set);

    void writeSummary(string out_name);
    void writeSummarytable(string out_name);//cdy_add
    void writeGenePairs4GD(string out_name);
    void writeGenePairs4Ortholog(string out_name);
    void writeSingleGDPattern(string out_name);
    void writeSingleGDLineage(string out_name);
    void writeAncestralGDRetention(string out_name);
    void writeRecentGDRetention(string out_name);
    void writeMedianKs4GDs(string out_name);
    void writeRootedTrees(string out_folder);
    void writeGDtype(string out_name);//cdy_add

    void writeNewickTree(ofstream & os, tree<PhyNode> & curr_tree, tree<PhyNode>::iterator curr_it, long opt);

    void writeOmega4EachSpecies(string out_folder);
    void writeLowCopyOrthologs(string out_name1, string out_name2);
    void writePAML(string out_folder);
    void writeClusteredAncestors(string out_name);
    void writePhTrees(string out_name);//cdy_add

    void writeIsoformCandidates(string out_folder);
    void writeSisterClades(string out_name);

    void printTree(FILE* fp, tree<PhyNode>& sub_tree, long opt);
    void printSummarytable(FILE* fp, tree<PhyNode>& sub_tree);//cdy_add
    string phy_tree_file;
    string gene_idmap_file;
    string gene_tree_list_file;
    string out_folder;

    tree<PhyNode> phy_tree; //phytozome tree
    tree<PhyNode>::iterator phy_og; //outgroup on the phy tree
    vector<tree<PhyNode>::iterator> phy_nodes; //all nodes in a tree
    vector<tree<PhyNode>::iterator> phy_leaves; //leave nodes
    map<long,tree<PhyNode>::iterator> phy_index2node;
    map<long,long> phy_index2depth;

    map<string,string> gene_idmap;
    map<string, map<string,Omega> > gene2omega;
    vector<QPCluster> g_trees;
    vector<GeneDuplication> gds;
    set<string> genome_set;
    set<string> isoform_set;

    set<string> ignore4ortholog;
};

Tree2GD::Tree2GD(string t_file, string i_file, string l_file, string out_f) {
    phy_tree_file = t_file;
    gene_idmap_file = i_file;
    gene_tree_list_file = l_file;
    out_folder = out_f;

    if (access(out_folder.c_str(), 0) == -1) mkdir(out_folder.c_str(), 0777);
}

Tree2GD::~Tree2GD(){
}

void Tree2GD::execute() {
    //read a rooted species tree
    readNewickTree(phy_tree_file, phy_tree, phy_nodes, phy_leaves,"phyto");
    //read a list of gene tree files
    readTreeList(gene_tree_list_file, g_trees);
    //read a map of gene id to species name
    readGene2SpeciesMap(gene_idmap_file,gene_idmap);
    //read a quick-paranoid file when available
    if(QUICK_FILE != "") {
        vector<QPCluster> qp_clusters;
        readQuickParanoid(QUICK_FILE, qp_clusters,"node");
        for(long i=0;i<qp_clusters.size();i++) {
            g_trees.push_back(qp_clusters[i]);
//            printTree(stdout,qp_clusters[i].gene_tree,0);
        }
    }

    //read ka/ks information for gene pairs when available
    if(OMEGA_FILE != "") {
        readOmega(OMEGA_FILE, gene2omega);
    }

    if(GENOME_FILE != "") {
        readGenomeList(GENOME_FILE, genome_set);
    }
    if(ISOFORM_FILE != "") {
        readIgnoredIsoforms(ISOFORM_FILE, isoform_set);
    }

    printTree(stdout,phy_tree,0);
    //check species tree
    bool is_binary_tree=true;
    for(tree<PhyNode>::post_order_iterator a=phy_tree.begin_post();a!=phy_tree.end_post();a++) {
        if(a.number_of_children()>2) {
            cerr<<"ERROR: not a binary tree in the clade: "<<(*a).name<<endl;
            long num=0;
            for (tree<PhyNode>::sibling_iterator b = a.begin(); b != a.end(); b++) {
                cerr<<"subclade["<<(num+1)<<"]: ";
                for (tree<PhyNode>::leaf_iterator c = phy_tree.begin_leaf(b); c != phy_tree.end_leaf(b); c++) {
                    cerr<<" "<<(*c).name;
                }
                cerr<<endl;
                num++;
            }
            is_binary_tree=false;
        }
    }
    if(!is_binary_tree) exit(0);
    //set phy_index for phy_tree
    for(tree<PhyNode>::post_order_iterator a=phy_tree.begin_post();a!=phy_tree.end_post();a++) (*a).phy_index=(*a).index;
    //set outgroup for phy_tree
    phy_og=NULL;
    tree<PhyNode>::iterator it=phy_tree.begin();
    long min_num=phy_tree.size();
    for(tree<PhyNode>::sibling_iterator a=it.begin();a!=it.end();a++) {
        long leaf_num=0;
        for(tree<PhyNode>::leaf_iterator b=phy_tree.begin_leaf(a);b!=phy_tree.end_leaf(a);b++) {
            leaf_num++;
        }

        if(leaf_num<min_num) {
            phy_og=a;
            min_num=leaf_num;
        }
    }
    if(phy_og==NULL) phy_og=phy_tree.begin();
    cerr<<"outgroup: "<<(*phy_og).name<<endl;

//    map<long,set<long> > index2ancient;
//    for(tree<PhyNode>::post_order_iterator a=phy_tree.begin_post();a!=phy_tree.end_post();a++) {
//        if(a==phy_tree.begin()) break;
//        set<long> ancient;
//        tree<PhyNode>::iterator b=phy_tree.parent(a);
//
//        while(b!=phy_tree.begin()) {
//            ancient.insert((*b).index);
//            b=phy_tree.parent(b);
//        }
//        index2ancient[(*a).index]=ancient;
//    }

    map<string,long> name2phy_index;
    for(tree<PhyNode>::leaf_iterator a=phy_tree.begin_leaf(); a!=phy_tree.end_leaf(); a++) {
        name2phy_index[(*a).name]=(*a).index;
//        cout<<(*a).name<<"\t"<<(*a).index<<endl;
    }

    for(tree<PhyNode>::post_order_iterator a=phy_tree.begin_post(); a!=phy_tree.end_post(); a++) {
        phy_index2node[(*a).index]=a;
        phy_index2depth[(*a).index]=phy_tree.depth(a);
    }


//    map<long, set<long> > inherit;
//    for(tree<PhyNode>::post_order_iterator a=phy_tree.begin_post();a!=phy_tree.end_post();a++) {
//        set<long> set1;
//        for(tree<PhyNode>::sibling_iterator b=a.begin();b!=a.end();b++) {
//            for(set<long>::iterator c=inherit[(*b).phy_index].begin();c!=inherit[(*b).phy_index].end();c++) set1.insert(*c);
//        }
//        set1.insert((*a).phy_index);
//        inherit[(*a).phy_index]=set1;
//    }
//
//    for (tree<PhyNode>::iterator b = phy_tree.begin(); b != phy_tree.end(); b++) {
//        for (tree<PhyNode>::iterator c = phy_tree.begin(); c != phy_tree.end(); c++) {
//            if (b == c) continue;
//            if (inherit[(*b).phy_index].count((*c).phy_index) > 0 || inherit[(*c).phy_index].count((*b).phy_index) > 0) continue;
//            cout<<(*b).name<<"\t"<<(*c).name<<endl;
//        }
//    }

    cerr<<"loading "<<g_trees.size()<<" trees"<<endl;
    for(long i=0;i<g_trees.size();i++) {
        if(g_trees.size()>100 && i%(g_trees.size()/100)==0) cerr<<"  "<<i<<" of "<<g_trees.size()<<endl;
//        cout<<"["<<i<<"]\t"<<g_trees[i].tree_id<<"\t"<<g_trees[i].is_true_tree<<endl;
        if(!g_trees[i].is_true_tree) continue;
        vector<tree<PhyNode>::iterator> nodes;
        vector<tree<PhyNode>::iterator> leaves;
        //read a gene tree from file
        readNewickTree(g_trees[i].tree_file, g_trees[i].gene_tree, nodes, leaves, "node");
//        printTree(stdout,g_trees[i].gene_tree,0);
        //check gene name
        long leaf_num=0;
        vector<tree<PhyNode>::iterator> del_nodes_vec;
        for(tree<PhyNode>::leaf_iterator a=g_trees[i].gene_tree.begin_leaf(); a!=g_trees[i].gene_tree.end_leaf(); a++) {
            leaf_num++;
            if(gene_idmap.count((*a).name)==0) {
                fprintf(stderr, "warning[1], gene id not found in idmap: %s\n", (*a).name.c_str());
                del_nodes_vec.push_back(a);
                continue;
            }
            string name=gene_idmap[(*a).name];

            if(name2phy_index.count(name)==0) {
                fprintf(stderr, "warning[2], species name not found in the species tree: %s\n", name.c_str());
                del_nodes_vec.push_back(a);
                continue;
            }

            if(isoform_set.count((*a).name)) {
                del_nodes_vec.push_back(a);
                continue;
            }
        }

//        printTree(stdout,g_trees[i].gene_tree,0);
//        cout<<leaf_num<<" "<<del_nodes_vec.size()<<endl;
        if(del_nodes_vec.size()>0) {
            fprintf(stderr, "remove %ld nodes from tree: %s\n", del_nodes_vec.size(),g_trees[i].tree_file.c_str());
            if(leaf_num-del_nodes_vec.size()<2) {
                fprintf(stderr,"num of left leaves < 2, ignoring this tree.\n");
                g_trees[i].save=false;
            } else deleteNodes(g_trees[i].gene_tree, del_nodes_vec);
        }

        if(!g_trees[i].save) continue;
//        printTree(stdout,g_trees[i].gene_tree,0);

        set<long> species_cov;
        for(tree<PhyNode>::leaf_iterator a=g_trees[i].gene_tree.begin_leaf(); a!=g_trees[i].gene_tree.end_leaf(); a++) {
            g_trees[i].gene_ids.push_back((*a).name);
            string name=gene_idmap[(*a).name];
            (*a).phy_index=name2phy_index[name];
            species_cov.insert((*a).phy_index);
        }

        g_trees[i].species_num=species_cov.size();
//        cerr<<g_trees[i].tree_id<<"\t"<<g_trees[i].gene_ids.size()<<endl;
        //set index on the species for each node on the gene tree
        setPhyIndex(g_trees[i].gene_tree);

        tree<PhyNode>::pre_order_iterator og_it=NULL;
        if(ROOT_METHOD==KW_MIN_TOPO_ERR) {
            og_it=findRootWithMinTopoError(g_trees[i].gene_tree);
        } else if(ROOT_METHOD==KW_MAX_DUP_SCORE) {
            og_it=findRootWithMaxScore(g_trees[i].gene_tree);
            if(og_it==NULL) og_it=findRootWithMinTopoError(g_trees[i].gene_tree);
        } else if (ROOT_METHOD==KW_MAX_DUP_BRANCH) {
            og_it=findRootWithMaxScoreAndDist(g_trees[i].gene_tree);
            if(og_it==NULL) og_it=findRootWithMinTopoError(g_trees[i].gene_tree);
        } else {
            cerr<<"Error[1]: "<<ROOT_METHOD<<endl;
            exit(0);
        }

        //re-root the gene tree according to the position of the root node

        if(og_it!=NULL) {
            if(PRINT) cerr<<"root="<<(*og_it).name<<"\t"<<gene_idmap[(*og_it).name]<<endl;
            reRootTree(g_trees[i].gene_tree,og_it);
        } else {
            cerr<<"root not found: "<<g_trees[i].tree_file<<endl;
        }
//        printTree(stdout,g_trees[i].gene_tree,0);
    }

    //set phy_index again for all rooted trees including qp_clusters
    cerr<<"set index for "<<g_trees.size()<<" trees"<<endl;
    for(long i=0;i<g_trees.size();i++) {
        if(!g_trees[i].save) continue;
        setPhyIndex(g_trees[i].gene_tree);
    }

    //split a complex gene tree into several simple sub-trees
    if(SPLIT_TREE) splitClusters();

    for(long i=0;i<g_trees.size();i++) {
        if(!g_trees[i].save) continue;
        g_trees[i].top_phy_index=(*g_trees[i].gene_tree.begin()).phy_index;
//        cerr<<g_trees[i].tree_id<<"\t"<<g_trees[i].gene_ids.size()<<endl;
    }

//    double SPECIES_COV=0.85;
//    //check species coverage for gene trees
//    long pass_trees=0;
//    for(long i=0;i<g_trees.size();i++) {
//        if(1.0 * g_trees[i].species_num / phy_leaves.size() < SPECIES_COV) g_trees[i].save=false;
//        else pass_trees++;
//    }
//    cerr<<pass_trees<<" of "<<g_trees.size()<<" trees pass the filter of species coverage"<<endl;

    //find GDs
    cerr<<"identifying gene duplications"<<endl;
    for(long i=0;i<g_trees.size();i++) {
        if(!g_trees[i].save) continue;
//        cerr<<"[tree "<<g_trees[i].tree_id<<"]\t"<<g_trees[i].tree_file<<endl;
        if(g_trees.size()>100 && i%(g_trees.size()/100)==0) cout<<"  "<<i<<" of "<<g_trees.size()<<endl;
        if(PRINT) printTree(stdout,g_trees[i].gene_tree,1);

        //a map for GDs in child node (node_index [not phy_index] to gd_id)
        map<long,long> child_gd;

        set<long> N0_set;
        set<long> gd_node_set;
        //iterating each node on the gene tree for possible GDs
        for (tree<PhyNode>::post_order_iterator it = g_trees[i].gene_tree.begin_post();it != g_trees[i].gene_tree.end_post();it++) {
//            cout<<(*it).name<<"\t"<<(*it).index<<endl;
            if(!(*it).save) continue;

            N0_set.insert((*it).index);

            if(it.number_of_children()<2) {
                continue;
            }

            if(PRINT) cout<<"===== checking: "<<(*it).name<<endl;

            //collect information for sub-branches
            vector<map<long, vector<string> > > clade_leafs;    //leafs for each of 2 clades, map of species2gene_id_vec
            vector<set<long> > clade_nodes;                //sub-nodes for each of 2 clades
            vector<tree<PhyNode>::iterator> clade_iterator;
            for (tree<PhyNode>::sibling_iterator a = it.begin(); a != it.end(); a++) {
                map<long, vector<string> > map1;
//                cout << "#" <<(*a).name << endl;
                if(a.number_of_children() == 0) {
                    vector<string> vec1;
                    vec1.push_back((*a).name);
                    long s_index=(*a).phy_index;
                    map1[s_index]=vec1;
                } else {
                    for (tree<PhyNode>::leaf_iterator b = g_trees[i].gene_tree.begin_leaf(a); b != g_trees[i].gene_tree.end_leaf(a); b++) {
                        long s_index=(*b).phy_index;
                        if(map1.count(s_index)==0) {
                            vector<string> vec1;
                            vec1.push_back((*b).name);
                            map1[s_index]=vec1;
                        } else map1[s_index].push_back((*b).name);
                    }
                }
                clade_leafs.push_back(map1);

                tree<PhyNode>::iterator top=phy_index2node[(*it).phy_index];

                set<long> set1;
                for(map<long, vector<string> >::iterator b=map1.begin();b!=map1.end();b++) {
                    //all of nodes from this leaf to lca are included (gene retention)
                    tree<PhyNode>::iterator c=phy_index2node[b->first];
                    while(c!=top) {
                        set1.insert((*c).phy_index);
                        c=phy_tree.parent(c);
                    }
                }
                clade_nodes.push_back(set1);
                clade_iterator.push_back(a);
            }

            //get leaf number under this node
            long leaf_num=0;
            for (tree<PhyNode>::leaf_iterator a = phy_tree.begin_leaf(phy_index2node[(*it).phy_index]); a != phy_tree.end_leaf(phy_index2node[(*it).phy_index]); a++) {
                leaf_num++;
            }

            if(PRINT) cout<<" clades= "<<clade_leafs.size()<<" specices="<<leaf_num<<endl;
            //find overlapped species between pair of branches
            bool find_gd=false;
            for(long a=0;a<clade_leafs.size()-1;a++) {
                for(long b=a+1;b<clade_leafs.size();b++) {
                    //check overlap
                    vector<long> overlap;
                    for(map<long, vector<string> >::iterator c=clade_leafs[a].begin();c!=clade_leafs[a].end();c++) {
                        if(clade_leafs[b].count(c->first)>0) overlap.push_back(c->first);
                    }

                    if(PRINT) cout<<"==="<<overlap.size()<<"\t"<<clade_leafs[a].size()<<"\t"<<clade_leafs[b].size()<<endl;

                    bool is_gd=false;
                    long depth_var=0;
                    long overlap_lca_index=-1;

                    if(leaf_num<2) {    //single species duplication
                        if(overlap.size()>0) {
                            overlap_lca_index=(*it).phy_index;
                            is_gd=true;
                        }
                    } else if(leaf_num==2) {    //two species duplication
                        if(overlap.size()>0) {
                            if(overlap.size()==1) {
                                overlap_lca_index=overlap[0];
                                depth_var=1;
                            } else {
                                overlap_lca_index=(*it).phy_index;
                                depth_var=0;
                            }
                            is_gd=true;
                        }
                    } else if(overlap.size() >= MIN_SPECIES) {  //ancient duplications before diversification of three or more species
                        //find LCA
                        long min_index = phy_tree.size();
                        long max_index = -1;

                        for(long c=0;c<overlap.size();c++) {
                            if (min_index > overlap[c]) min_index = overlap[c];
                            if (max_index < overlap[c]) max_index = overlap[c];
                        }
                        tree<PhyNode>::iterator lca = getLCA(phy_tree, min_index, max_index);
                        overlap_lca_index=(*lca).phy_index;
                        depth_var=phy_index2depth[(*lca).phy_index]-phy_index2depth[(*it).phy_index];

                        if(depth_var<=MAX_DEEP_VAR) is_gd=true;

                        if(PRINT) cout<<" lca="<<(*lca).name<<"\tdist="<<depth_var<<"\t"<<phy_index2depth[(*lca).phy_index]<<"\t"<<phy_index2depth[(*it).phy_index]<<endl;
                    }

                    //for orhtolog prediction
//                    if(leaf_num>1 && overlap.size()>0 && (clade_leafs[a].size()==1 || clade_leafs[b].size()==1)) {
//                        map<long, vector<string> >::iterator m=clade_leafs[a].begin();
//
//                        if(clade_leafs[a].size()==1) m=clade_leafs[a].begin();
//                        else m=clade_leafs[b].begin();
//
//                        for(long n=0;n<m->second.size();n++) {
//                            ignore4ortholog.insert(m->second[n]);
////                            cout<<"ignore: "<<m->second[n]<<endl;
//                        }
//                    }

                    if(!is_gd) continue;
                    //creat a new duplication
//                    (*phy_index2node[(*it).phy_index]).gd_count++;

                    //set info for a GD
                    GeneDuplication gd;
                    gd.gd_id=gds.size();
                    gd.gene_tree_id = g_trees[i].tree_id;
                    gd.gene_tree_node=it;
//                    gd.node_name = gene_idmap[(*it).name];
                    gd.phy_index = (*it).phy_index;
                    gd.overlap_lca_index=overlap_lca_index;

                    for(set<long>::iterator c=clade_nodes[a].begin();c!=clade_nodes[a].end();c++) gd.clade1.insert((*c));
                    for(set<long>::iterator c=clade_nodes[b].begin();c!=clade_nodes[b].end();c++) gd.clade2.insert((*c));

                    for(long c=0;c<overlap.size();c++) {
                        for(long x1=0;x1<clade_leafs[a][overlap[c]].size();x1++) {
                            for(long x2=0;x2<clade_leafs[b][overlap[c]].size();x2++) {
                                Pair p;
                                p.species_id=(*phy_index2node[overlap[c]]).name;
                                p.gene1=clade_leafs[a][overlap[c]][x1];
                                p.gene2=clade_leafs[b][overlap[c]][x2];
                                gd.gene_pairs.push_back(p);
                            }
                        }
                    }

//                    gd.multiple=0;
                    gd.ks=-1;
                    gd.depth_var=depth_var;
                    gd.comment="_";

                    gd.this_bp=(*it).bootstrap;
                    gd.child_bp1=(*clade_iterator[a]).bootstrap;
                    gd.child_bp2=(*clade_iterator[b]).bootstrap;

                    gd.median_clade_len1=0;
                    gd.median_clade_len2=0;

                    if(clade_iterator[a].number_of_children()<2) {
                        gd.median_clade_len1=(*clade_iterator[a]).dist;
//                        cout<<gd.median_clade_len1<<endl;
                    } else {
                        vector<double> len_vec;
                        for (tree<PhyNode>::leaf_iterator c = phy_tree.begin_leaf(clade_iterator[a]); c != phy_tree.end_leaf(clade_iterator[a]); c++) {
                            double len = 0;
                            tree<PhyNode>::iterator d = c;
                            while (d != it) {
                                len += (*d).dist;
                                d = phy_tree.parent(d);
                            }
                            len += (*d).dist;
                            len_vec.push_back(len);
//                            cout << (*c).name << "\t" << len << endl;
                        }
                        if (len_vec.size() > 0) {
                            quickSortDouble(len_vec, 0, len_vec.size() - 1, true);
                            gd.median_clade_len1 = quantile(len_vec, 0.5);
//                            cout << gd.median_clade_len1 << endl;
                        }
                    }

                    if(clade_iterator[b].number_of_children()<2) {
                        gd.median_clade_len2=(*clade_iterator[b]).dist;
//                        cout<<gd.median_clade_len2<<endl;
                    } else {
                        vector<double> len_vec;
                        for (tree<PhyNode>::leaf_iterator c = phy_tree.begin_leaf(clade_iterator[b]); c != phy_tree.end_leaf(clade_iterator[b]); c++) {
                            double len = 0;
                            tree<PhyNode>::iterator d = c;
                            while (d != it) {
                                len += (*d).dist;
                                d = phy_tree.parent(d);
                            }
                            len += (*d).dist;
                            len_vec.push_back(len);
//                            cout << (*c).name << "\t" << len << endl;
                        }
                        if (len_vec.size() > 0) {
                            quickSortDouble(len_vec, 0, len_vec.size() - 1, true);
                            gd.median_clade_len2 = quantile(len_vec, 0.5);
//                            cout << gd.median_clade_len2 << endl;
                        }
                    }

                    gd.save=true;

                    child_gd[(*it).index]=gd.gd_id;
//                    cout<<">"<<(*it).name<<" "<<(gds.size()+1)<<endl;

                    //check if the child nodes have further GD
                    if(it.number_of_children()>1) {
                        tree<PhyNode>::sibling_iterator m=it.begin();
//                        cout<<" ."<<(*m).name<<", "<<child_gd.count((*m).index)<<endl;
                        if (child_gd.count((*m).index) > 0) gd.child_gd1.push_back(child_gd[(*m).index]);
                        for (tree<PhyNode>::pre_order_iterator n = m.begin(); n != m.end(); n++) {
//                            cout<<" ."<<(*n).name<<", "<<child_gd.count((*n).index)<<endl;
                            if (child_gd.count((*n).index) > 0) gd.child_gd1.push_back(child_gd[(*n).index]);
                        }

                        m++;
//                        cout<<" ."<<(*m).name<<", "<<child_gd.count((*m).index)<<endl;
                        if (child_gd.count((*m).index) > 0) gd.child_gd1.push_back(child_gd[(*m).index]);
                        for (tree<PhyNode>::pre_order_iterator n = m.begin(); n != m.end(); n++) {
//                            cout<<" :"<<(*n).name<<", "<<child_gd.count((*n).index)<<endl;
                            if (child_gd.count((*n).index) > 0) gd.child_gd2.push_back(child_gd[(*n).index]);
                        }
                    }
//                    cout<<(*phy_index2node[gd.phy_index]).name<<"\t"<<gd.child_gd1.size()<<","<<gd.child_gd2.size()<<endl;

                    find_gd=true;
                    gds.push_back(gd);
                }
            }

            if(find_gd) {   //remove N0 of child if: child.phyindex == parent.phyindex; child.index is saved in the set; child doesn't have a GD
                gd_node_set.insert((*it).index);
                for (tree<PhyNode>::sibling_iterator b = it.begin(); b != it.end(); b++) {
                    if((*it).phy_index==(*b).phy_index && N0_set.count((*b).index)>0 && gd_node_set.count((*b).index)==0) N0_set.erase((*b).index);
                }
            }
//            else {    //remove N0 of child if this.index is saved in the set and this.phyindex == parent.phyindex
//                for (tree<PhyNode>::sibling_iterator b = it.begin(); b != it.end(); b++) {
//                    if((*it).phy_index==(*b).phy_index && N0_set.count((*b).index)>0 && gd_node_set.count((*b).index)==0) N0_set.erase((*b).index);
//                }
//            }
        }

        set<long> visited;
        set<long> ignored;
        for (tree<PhyNode>::post_order_iterator it = g_trees[i].gene_tree.begin_post();it != g_trees[i].gene_tree.end_post();it++) {
            if((*it).bootstrap<MIN_BOOTSTRAP) {
                (*it).save=false;
                continue;
            }
            visited.insert((*it).phy_index);

            if(gd_node_set.count((*it).index)>0) (*phy_index2node[(*it).phy_index]).lineage_count++;
            else if(N0_set.count((*it).index)>0) {
                if(ignored.count((*it).index)==0) {
                    (*phy_index2node[(*it).phy_index]).lineage_count++;
                }
                if(it!=g_trees[i].gene_tree.begin()) {
                    tree<PhyNode>::iterator parent=g_trees[i].gene_tree.parent(it);
                    if((*parent).phy_index==(*it).phy_index) ignored.insert((*parent).index);
                }
            }
        }

        for(set<long>::iterator j=visited.begin();j!=visited.end();j++) {
            (*phy_index2node[*j]).tree_count++;
        }
    }

    //filter GDs
    for(long i=0;i<gds.size();i++) {
        if(gds[i].this_bp<MIN_BOOTSTRAP || gds[i].child_bp1<MIN_SUB_CLADE_BP || gds[i].child_bp2<MIN_SUB_CLADE_BP) gds[i].save=false;
    }

    //set kaks for each GD
    if(gene2omega.size()>0) {
        cerr<<"collect ka ks for "<<gds.size()<<" gds"<<endl;
        setMinKaKs4GDs();
    }

    //adjust GDs based on ks
    if(gene2omega.size()>0) {
        cerr<<"adjust LCA for "<<gds.size()<<" gds"<<endl;
        adjustGDsByKs2();
    }

    //collect GDs counts on the species tree
    for(long i=0;i<gds.size();i++) {
        if(gds[i].save) {
            (*phy_index2node[gds[i].phy_index]).gd_count++;
        }
    }

    //save outgroup ids for clusters (whose top_phy_index == top), else save outgroup from function addExtraRoot();
    for (long i = 0; i < g_trees.size(); i++) {
        if(!g_trees[i].save) continue;
        for (tree<PhyNode>::leaf_iterator a = g_trees[i].gene_tree.begin_leaf(); a != g_trees[i].gene_tree.end_leaf(); a++) {
            if(gene_idmap.count((*a).name)==0) continue;
            if (gene_idmap[(*a).name] == (*phy_og).name) g_trees[i].og_ids.push_back((*a).name);
        }
    }

//    for (long i = 0; i < g_trees.size(); i++) cout<<g_trees[i].tree_id+": "<<g_trees[i].og_ids.size()<<endl;
    if(PARSER_FILE != "") {
        addExtraRoot();
    }
//    for (long i = 0; i < g_trees.size(); i++) cout<<g_trees[i].tree_id+": "<<g_trees[i].og_ids.size()<<endl;

    cerr<<"validate and output files"<<endl;
//    bool check=getWebTime();
//    if(!check) return;

    writeSummary(out_folder+"/summary.txt");

    writeLowCopyOrthologs(out_folder+"/low_copy_orthologs.info",out_folder+"/low_copy_orthologs.quick");
    writeGenePairs4GD(out_folder+"/gd.gene_pairs.txt");
    writeGenePairs4Ortholog(out_folder+"/ortholog.gene_pairs.txt");

    writeSingleGDPattern(out_folder+"/gd.single_gd_pattern.txt");
    writeSingleGDLineage(out_folder+"/gd.single_gd_lineage.txt");

    writeAncestralGDRetention(out_folder+"/gd.ancestral_gd_retention.txt");
    writeRecentGDRetention(out_folder+"/gd.recent_gd_retention.txt");
    writeMedianKs4GDs(out_folder+"/gd.median_ks.txt");
    writeGDtype(out_folder+"/GDtype_stat.txt");//cdy_add
    writeSummarytable(out_folder+"/summarytable.txt");//cdy_add
    writePhTrees(out_folder+"/Phtree.nwk");//cdy_add


//    if(gene2omega.size()>0) writeOmega4EachSpecies(out_folder);
    if(SAVE_ROOTED) writeRootedTrees(out_folder);
    writeClusteredAncestors(out_folder+"/clusters.ancestors.txt");
    writeIsoformCandidates(out_folder);
    writeSisterClades(out_folder+"/sister_clades.txt");

    if(SAVE_PAML) writePAML(out_folder);

//    printTree(stdout,phy_tree,0);
}

tree<PhyNode>::iterator Tree2GD::findRootWithMinTopoError(tree<PhyNode> & curr_tree) {
    tree<PhyNode>::iterator og=NULL;
    double min_gd_num=curr_tree.size();
    if(min_gd_num<phy_tree.size()) min_gd_num=phy_tree.size();

    if(PRINT) printTree(stdout,curr_tree,2);
    //find LCA
//    long min_index = phy_tree.size();
//    long max_index = -1;
//
//    for (tree<PhyNode>::leaf_iterator a = curr_tree.begin_leaf(); a != curr_tree.end_leaf(); a++) {
//        if (min_index > (*a).phy_index) min_index = (*a).phy_index;
//        if (max_index < (*a).phy_index) max_index = (*a).phy_index;
//    }
////    cerr << min_index << "\t" << max_index << endl;
//    tree<PhyNode>::iterator lca = getLCA(phy_tree, min_index, max_index);
//
//    if(PRINT) cerr<<"lca: "<<(*lca).name<<endl;
//    printTree(stdout,curr_tree,2);
    for(tree<PhyNode>::pre_order_iterator i=curr_tree.begin();i!=curr_tree.end();i++) {
        if(i==curr_tree.begin()) continue;
        tree<PhyNode> temp_tree;
        temp_tree.insert_subtree(temp_tree.begin(),curr_tree.begin());

//        copy(curr_tree.begin(),curr_tree.end(),temp_tree.begin());
        tree<PhyNode>::iterator temp_og=temp_tree.begin();
        while(temp_og!=temp_tree.end()) {
            if((*temp_og).index==(*i).index) break;
            temp_og++;
        }
        reRootTree(temp_tree,temp_og);
//        cout<<"***"<<(*i).name<<endl;
//        printTree(stdout,temp_tree,2);

        double gd_num=0;
        //get duplication number
        for(tree<PhyNode>::pre_order_iterator j=temp_tree.begin();j!=temp_tree.end();j++) {
            bool has_gd=false;
            for(tree<PhyNode>::sibling_iterator k=j.begin();k!=j.end();k++) {
                if((*k).phy_index==(*j).phy_index) has_gd=true;
            }
            if(has_gd) {
                gd_num+=1.0/(phy_index2depth[(*j).phy_index]+1);
//                cout<<"   gd="<<(*j).name<<", weight="<<phy_index2depth[(*j).phy_index]<<endl;
            }
        }
        if(gd_num<min_gd_num) {
            og=i;
            min_gd_num=gd_num;
        }
//        cout<<"gd="<<gd_num<<" "<<(*i).name<<endl;
    }
    if(PRINT) cout<<"outgroup: "<<(*og).name<<"\t"<<gene_idmap[(*og).name]<<endl;
    return og;
}

tree<PhyNode>::iterator Tree2GD::findRootWithMaxScore(tree<PhyNode> & curr_tree) {
    tree<PhyNode>::iterator og=NULL;
    double max_score=0;

    if(PRINT) printTree(stdout,curr_tree,2);
//    printTree(stdout,curr_tree,2);

    //find LCA
    long min_index = phy_tree.size();
    long max_index = -1;

    set<long> leaves;
    for (tree<PhyNode>::leaf_iterator a = curr_tree.begin_leaf(); a != curr_tree.end_leaf(); a++) {
        if (min_index > (*a).phy_index) min_index = (*a).phy_index;
        if (max_index < (*a).phy_index) max_index = (*a).phy_index;
        leaves.insert((*a).phy_index);
    }

    tree<PhyNode>::iterator lca = getLCA(phy_tree, min_index, max_index);
//    cout << "LCA: "<<(*lca).name<<"\t"<<min_index << "\t" << max_index << endl;

    if(lca.number_of_children()<2) return og;

    set<long> phy_set0; //0 and 1 are either ingroup or outgroup
    set<long> phy_set1;
    tree<PhyNode>::sibling_iterator it0=lca.begin();
    tree<PhyNode>::sibling_iterator it1=it0;
    it1++;

    if(it0.number_of_children()==0) {
        if(leaves.count((*it0).phy_index)>0) phy_set0.insert((*it0).phy_index);
    } else for(tree<PhyNode>::leaf_iterator a=phy_tree.begin_leaf(it0);a!=phy_tree.end_leaf(it0);a++) {
        if(leaves.count((*a).phy_index)>0) phy_set0.insert((*a).phy_index);
    }

    if(it1.number_of_children()==0) {
        if(leaves.count((*it1).phy_index)>0) phy_set1.insert((*it1).phy_index);
    } else for(tree<PhyNode>::leaf_iterator a=phy_tree.begin_leaf(it1);a!=phy_tree.end_leaf(it1);a++) {
        if(leaves.count((*a).phy_index)>0) phy_set1.insert((*a).phy_index);
    }

    if(phy_set0.size()==0 || phy_set1.size()==0) return og;

//    cout<<"set0: ";
//    for(set<long>::iterator a=phy_set0.begin();a!=phy_set0.end();a++) cout<<(*phy_index2node[*a]).name<<" ";
//    cout<<endl;
//
//    cout<<"set1: ";
//    for(set<long>::iterator a=phy_set1.begin();a!=phy_set1.end();a++) cout<<(*phy_index2node[*a]).name<<" ";
//    cout<<endl;

    double scores[2][2];
    for(long m=0;m<2;m++) {
        for(long n=0;n<2;n++) scores[m][n]=0;
    }

    for(tree<PhyNode>::pre_order_iterator i=curr_tree.begin();i!=curr_tree.end();i++) {
        if(i==curr_tree.begin()) continue;
//        cout<<"===check node: "<<(*i).name<<endl;

        set<long> sub_leaves0;
        set<long> sub_leaves1;
        set<long> sub0_its; //record index, NOT phy_index

        if(i.number_of_children()==0) {
            sub_leaves0.insert((*i).phy_index);
            sub0_its.insert((*i).index);
        } else {
            for (tree<PhyNode>::leaf_iterator a = curr_tree.begin_leaf(i); a != curr_tree.end_leaf(i); a++) {
                sub_leaves0.insert((*a).phy_index);
                sub0_its.insert((*a).index);
            }
        }

        for(tree<PhyNode>::leaf_iterator a=curr_tree.begin_leaf();a!=curr_tree.end_leaf();a++) {
            if(sub0_its.count((*a).index)==0) sub_leaves1.insert((*a).phy_index);
        }

//        cout<<"left: ";
//        for(set<long>::iterator a=sub_leaves0.begin();a!=sub_leaves0.end();a++) cout<<(*phy_index2node[*a]).name<<" ";
//        cout<<endl;
//
//        cout<<"right: ";
//        for(set<long>::iterator a=sub_leaves1.begin();a!=sub_leaves1.end();a++) cout<<(*phy_index2node[*a]).name<<" ";
//        cout<<endl;

        for(long m=0;m<2;m++) {
            for(long n=0;n<2;n++) scores[m][n]=0;
        }

        scores[0][0]=1.0*intersect(phy_set0,sub_leaves0)/phy_set0.size();
        scores[0][1]=1.0*intersect(phy_set0,sub_leaves1)/phy_set0.size();
        scores[1][0]=1.0*intersect(phy_set1,sub_leaves0)/phy_set1.size();
        scores[1][1]=1.0*intersect(phy_set1,sub_leaves1)/phy_set1.size();

//        cout<<"raw: "<<scores[0][0]<<"\t"<<scores[0][1]<<"\t"<<scores[1][0]<<"\t"<<scores[1][1]<<endl;

        double io_score0=scores[0][0]*scores[1][1]*(1-scores[0][1])*(1-scores[1][0]);
        double io_score1=scores[0][1]*scores[1][0]*(1-scores[0][0])*(1-scores[1][1]);
        double ad_score=scores[0][0]*scores[1][1]*scores[0][1]*scores[1][0];

        double score=max(io_score0,io_score1);
        score=max(score,ad_score);

        if(max_score<score) {
            og=i;
            max_score=score;
        }
//        cout<<"score: "<<score<<"\t"<<(*i).name<<"\t"<<(*i).dist<<endl;
    }
    if(PRINT) cout<<"outgroup: "<<(*og).name<<"\t"<<gene_idmap[(*og).name]<<endl;
    return og;
}

tree<PhyNode>::iterator Tree2GD::findRootWithMaxScoreAndDist(tree<PhyNode> & curr_tree) {
    tree<PhyNode>::iterator og=NULL;
    double max_score=0;

    if(PRINT) printTree(stdout,curr_tree,2);
//    printTree(stdout,curr_tree,2);

    //find LCA
    long min_index = phy_tree.size();
    long max_index = -1;

    set<long> leaves;
    for (tree<PhyNode>::leaf_iterator a = curr_tree.begin_leaf(); a != curr_tree.end_leaf(); a++) {
        if (min_index > (*a).phy_index) min_index = (*a).phy_index;
        if (max_index < (*a).phy_index) max_index = (*a).phy_index;
        leaves.insert((*a).phy_index);
    }

    tree<PhyNode>::iterator lca = getLCA(phy_tree, min_index, max_index);
//    cout << "LCA: "<<(*lca).name<<"\t"<<min_index << "\t" << max_index << endl;

    if(lca.number_of_children()<2) return og;

    set<long> phy_set0; //0 for outgroup
    set<long> phy_set1; //1 for ingroup

    while(phy_set0.size()<2) {
        if(lca.number_of_children()<2) return og;
        tree<PhyNode>::sibling_iterator it0=lca.begin();
        tree<PhyNode>::sibling_iterator it1=it0;
        it1++;

        set<long> set0;
        set<long> set1;

        if(it0.number_of_children()==0) {
            if(leaves.count((*it0).phy_index)>0) set0.insert((*it0).phy_index);
        } else for(tree<PhyNode>::leaf_iterator a=phy_tree.begin_leaf(it0);a!=phy_tree.end_leaf(it0);a++) {
            if(leaves.count((*a).phy_index)>0) set0.insert((*a).phy_index);
        }

        if(it1.number_of_children()==0) {
            if(leaves.count((*it1).phy_index)>0) set1.insert((*it1).phy_index);
        } else for(tree<PhyNode>::leaf_iterator a=phy_tree.begin_leaf(it1);a!=phy_tree.end_leaf(it1);a++) {
            if(leaves.count((*a).phy_index)>0) set1.insert((*a).phy_index);
        }

        if(set0.size()<set1.size()) {
            for(set<long>::iterator a=set0.begin();a!=set0.end();a++) phy_set0.insert(*a);
            lca=it1;
        } else {
            for(set<long>::iterator a=set1.begin();a!=set1.end();a++) phy_set0.insert(*a);
            lca=it0;
        }
    }

    if(lca.number_of_children()==0) {
        if(leaves.count((*lca).phy_index)>0) phy_set1.insert((*lca).phy_index);
    } else for(tree<PhyNode>::leaf_iterator a=phy_tree.begin_leaf(lca);a!=phy_tree.end_leaf(lca);a++) {
        if(leaves.count((*a).phy_index)>0) phy_set1.insert((*a).phy_index);
    }

    if(phy_set0.size()==0 || phy_set1.size()==0) return og;

//    cout<<"set0: ";
//    for(set<long>::iterator a=phy_set0.begin();a!=phy_set0.end();a++) cout<<(*phy_index2node[*a]).name<<" ";
//    cout<<endl;
//
//    cout<<"set1: ";
//    for(set<long>::iterator a=phy_set1.begin();a!=phy_set1.end();a++) cout<<(*phy_index2node[*a]).name<<" ";
//    cout<<endl;

    double scores[2][2];
    for(long m=0;m<2;m++) {
        for(long n=0;n<2;n++) scores[m][n]=0;
    }

    for(tree<PhyNode>::pre_order_iterator i=curr_tree.begin();i!=curr_tree.end();i++) {
        if(i==curr_tree.begin()) continue;
//        cout<<"===check node: "<<(*i).name<<endl;

        set<long> sub_leaves0;
        set<long> sub_leaves1;
        set<long> sub0_its; //record index, NOT phy_index

        if(i.number_of_children()==0) {
            sub_leaves0.insert((*i).phy_index);
            sub0_its.insert((*i).index);
        } else {
            for (tree<PhyNode>::leaf_iterator a = curr_tree.begin_leaf(i); a != curr_tree.end_leaf(i); a++) {
                sub_leaves0.insert((*a).phy_index);
                sub0_its.insert((*a).index);
            }
        }

        for(tree<PhyNode>::leaf_iterator a=curr_tree.begin_leaf();a!=curr_tree.end_leaf();a++) {
            if(sub0_its.count((*a).index)==0) sub_leaves1.insert((*a).phy_index);
        }

//        cout<<"left: ";
//        for(set<long>::iterator a=sub_leaves0.begin();a!=sub_leaves0.end();a++) cout<<(*phy_index2node[*a]).name<<" ";
//        cout<<endl;
//
//        cout<<"right: ";
//        for(set<long>::iterator a=sub_leaves1.begin();a!=sub_leaves1.end();a++) cout<<(*phy_index2node[*a]).name<<" ";
//        cout<<endl;

        for(long m=0;m<2;m++) {
            for(long n=0;n<2;n++) scores[m][n]=0;
        }

        scores[0][0]=1.0*intersect(phy_set0,sub_leaves0)/phy_set0.size();
        scores[0][1]=1.0*intersect(phy_set0,sub_leaves1)/phy_set0.size();
        scores[1][0]=1.0*intersect(phy_set1,sub_leaves0)/phy_set1.size();
        scores[1][1]=1.0*intersect(phy_set1,sub_leaves1)/phy_set1.size();

//        cout<<"raw: "<<scores[0][0]<<"\t"<<scores[0][1]<<"\t"<<scores[1][0]<<"\t"<<scores[1][1]<<endl;

        double io_score0=scores[0][0]*scores[1][1]*(1-scores[0][1])*(1-scores[1][0]);
        double io_score1=scores[0][1]*scores[1][0]*(1-scores[0][0])*(1-scores[1][1]);

        double ad_score0=scores[0][0]*scores[1][1]*max(scores[0][1],scores[1][0]);
        double ad_score1=scores[0][1]*scores[1][0]*max(scores[0][0],scores[1][1]);

        double score=max(io_score0,io_score1);
        score=max(score,ad_score0);
        score=max(score,ad_score1);
        score*=sqrt((*i).dist);

        if(max_score<score) {
            og=i;
            max_score=score;
        }
//        cout<<"score: "<<score<<"\t"<<(*i).name<<"\t"<<(*i).dist<<endl;
    }
    if(PRINT) cout<<"outgroup: "<<(*og).name<<"\t"<<gene_idmap[(*og).name]<<endl;
    return og;
}

void Tree2GD::reRootTree(tree<PhyNode> & curr_tree, tree<PhyNode>::iterator outgroup) {
    if(PRINT) cerr<<"reRoot:\t"<<(*outgroup).name<<endl;
    tree<PhyNode> new_tree;
    tree<PhyNode>::iterator it1=outgroup;
//    printTree(stdout,curr_tree,2);

    //search from outgroup to current root,
    vector<tree<PhyNode>::iterator> vec;
    while(it1!=curr_tree.begin()) {
//        cerr<<"adding: "<<(*it1).name<<endl;
        vec.push_back(it1);
        it1=curr_tree.parent(it1);
    }
    if(PRINT) for(long i=0;i<vec.size();i++) cerr<<i<<":\t"<<(*vec[i]).name<<endl;

    for(long i=vec.size()-1;i>0;i--) {
        (*vec[i]).bootstrap=(*vec[i-1]).bootstrap;
        (*vec[i]).dist=(*vec[i-1]).dist;
    }
    (*outgroup).dist=0;

    tree<PhyNode>::iterator root=new_tree.insert(new_tree.begin(),(*curr_tree.begin())); //use the old root as a new root
    new_tree.append_child(root,outgroup); //add outgroup as the first child of root

    tree<PhyNode>::iterator parent;
    it1=outgroup;
    tree<PhyNode>::iterator it2=root;
    while(it1!=curr_tree.begin()) {
        parent=curr_tree.parent(it1);
        //insert parent node as child of it2, then let it2 points to this child
        if(parent!=curr_tree.begin()) {
            it2=new_tree.append_child(it2,(*parent));
//            cout<<"insert: "<<(*parent1).name<<", "<<(*parent1).bootstrap<<endl;
        }
        //append siblings of parent1 as child of it2, do not change it2's address
        for(tree<PhyNode>::sibling_iterator i=parent.begin();i!=parent.end();i++) {
            if(i==it1) continue;
            new_tree.append_child(it2,(tree<PhyNode>::iterator)i);
//            cout<<"append: "<<(*i).name<<", "<<(*i).bootstrap<<endl;
        }
//        printTree(stdout,new_tree,1);
        it1=parent;
    }

    //reset index for the new_tree
    setIndex(new_tree);
    setPhyIndex(new_tree);
    //reset outgroup according to the old id, because the old address doesn't work on the new tree
    for(tree<PhyNode>::post_order_iterator a= new_tree.begin_post();a != new_tree.end_post();a++) {
        if((*outgroup).name==(*a).name) outgroup=a;
    }
    if(PRINT) printTree(stdout,new_tree,2);
    //adjust length for the first split
    double bias,var,min;
    bias=var=min=0;
    evaluateTreeCenter(new_tree,outgroup,bias,var);

    min=0.01*bias;
    if(min<0.01) min=0.01;

    for (tree<PhyNode>::sibling_iterator i = root.begin(); i != root.end(); i++) {
        if (i == outgroup) {
            (*i).dist=bias;
        } else {
//            cerr << "dist1\t" << (*i).name << "\t" << (*i).dist << "\t" << (*outgroup).dist - bias << endl;
            (*i).dist = (*i).dist - bias;
            if ((*i).dist < min) (*i).dist = min;
        }
    }
//    cerr<<"dist2\t"<<(*outgroup).name<<"\t"<<(*outgroup).dist<<"\t"<<bias<<endl;

    curr_tree.clear();
    curr_tree.insert_subtree(curr_tree.begin(),new_tree.begin());
//    if(PRINT) printTree(stdout,curr_tree,1);
}

tree<PhyNode>::iterator Tree2GD::getLCA(tree<PhyNode> & curr_tree, long min_index, long max_index) {
    tree<PhyNode>::iterator lca = curr_tree.begin();

    if (min_index == max_index) {
        tree<PhyNode>::iterator it=curr_tree.begin();
        while(it!=curr_tree.end()) {
            if((*it).index==min_index) {
                lca=it;
                break;
            }
            it++;
        }
    } else {
        tree<PhyNode>::sibling_iterator it = lca.begin();
        while (it != lca.end()) {
//            cout<<(*it1).name<<" "<<(*it1).index<<endl;
            if ((*it).index < min_index) {
                it++;
            } else if ((*it).index > max_index) {
                lca = it;
                it = it.begin();
            } else break;
        }
    }
    return lca;
}

void Tree2GD::evaluateTreeCenter(tree<PhyNode> & curr_tree, tree<PhyNode>::iterator curr_node, double & bias, double & var) {
    vector<double> dist_vec1;
    vector<double> dist_vec2;

    for(tree<PhyNode>::leaf_iterator a=curr_tree.begin_leaf(); a!=curr_tree.end_leaf();a++) {
        bool is_include=false;
        tree<PhyNode>::iterator it=a;
        while(it!=curr_tree.begin()) {
            if(it==curr_node) {
                is_include=true;
                break;
            }
            it=curr_tree.parent(it);
        }
//        cerr<<(*a).name<<"\t"<<is_include<<endl;

        if(is_include) {
            double temp=distOfLeaf2Parent(curr_tree, curr_node, a);
            dist_vec1.push_back(temp);
        } else {
            long min_index=(*curr_node).index;
            long max_index=(*a).index;
            if(min_index>max_index) {
                long temp=min_index;
                min_index=max_index;
                max_index=temp;
            }
            tree<PhyNode>::iterator lca=getLCA(curr_tree, min_index, max_index);
//            cerr<<"lca: "<<(*lca).name<<"\t"<<(lca==curr_tree.begin())<<endl;

            double temp=distOfLeaf2Parent(curr_tree, lca, a)+distOfLeaf2Parent(curr_tree, lca, curr_node);
            dist_vec2.push_back(temp);
        }
    }

    double mean1=0;
    double mean2=0;
    for(long i=0;i<dist_vec1.size();i++) mean1+=dist_vec1[i];
    for(long i=0;i<dist_vec2.size();i++) mean2+=dist_vec2[i];

    if(dist_vec1.size()>0) mean1/=dist_vec1.size();
    if(dist_vec2.size()>0) mean2/=dist_vec2.size();

    bias=(mean1+mean2)/2-mean1;
//    cerr<<bias<<endl;
    if(bias<0) bias=0;

    double mean=0;
    for(long i=0;i<dist_vec1.size();i++) mean+=dist_vec1[i]+bias;
    for(long i=0;i<dist_vec2.size();i++) mean+=dist_vec2[i]-bias;
    if(dist_vec1.size()+dist_vec2.size()>0) mean=mean/(dist_vec1.size()+dist_vec2.size());

    for(long i=0;i<dist_vec1.size();i++) var+=(dist_vec1[i]+bias-mean)*(dist_vec1[i]+bias-mean);
    for(long i=0;i<dist_vec2.size();i++) var+=(dist_vec2[i]-bias-mean)*(dist_vec2[i]-bias-mean);
    var=sqrt(var);
    if(dist_vec1.size()+dist_vec2.size()>0) var=var/(dist_vec1.size()+dist_vec2.size());
//    cerr<<" ----- "<<(*curr_node).name<<"\t"<<bias<<"\t"<<var<<endl;
}

double Tree2GD::distOfLeaf2Parent(tree<PhyNode> & curr_tree, tree<PhyNode>::iterator parent_node, tree<PhyNode>::iterator leaf_node) {
    double dist=0;
    tree<PhyNode>::iterator it = leaf_node;
    while (it != parent_node) {
        dist += (*it).dist;
        it = curr_tree.parent(it);
    }
    return dist;
}

void Tree2GD::splitClusters() {
    long root_index=(*phy_tree.begin()).phy_index;

    vector<QPCluster> new_clusters;
    for (long a = 0; a < g_trees.size(); a++) {
        if(!g_trees[a].is_true_tree) {
            new_clusters.push_back(g_trees[a]);
            continue;
        }
//        printTree(stderr,g_trees[a].gene_tree,0);
        set<long> ignored;
        vector<QPCluster> temp_vec;
        for(tree<PhyNode>::post_order_iterator b = g_trees[a].gene_tree.begin_post(); b != g_trees[a].gene_tree.end_post(); b++) {
//            cerr<<(*b).phy_index<<", "<<(*b).name<<endl;
            if(ignored.count((*b).index)==0 && (*b).phy_index==root_index && (*b).bootstrap>=MIN_BOOTSTRAP && !(*b).is_leaf) {
                QPCluster qc;
                qc.tree_id = g_trees[a].tree_id;
                qc.tree_file = g_trees[a].tree_file;
                qc.top_phy_index = (*b).phy_index;
                qc.gene_tree.insert_subtree(qc.gene_tree.begin(), b);
                qc.species_num=0;
                qc.is_true_tree=true;
                qc.save=true;

                for(tree<PhyNode>::leaf_iterator leaf_it=qc.gene_tree.begin_leaf();leaf_it!=qc.gene_tree.end_leaf();leaf_it++) qc.gene_ids.push_back((*leaf_it).name);
                temp_vec.push_back(qc);
//                cerr<<"add"<<"\t"<<(*b).name<<endl;

                //insert parents
                for(tree<PhyNode>::iterator c=b;c!=g_trees[a].gene_tree.begin();c=g_trees[a].gene_tree.parent(c)) {
                    ignored.insert((*c).index);
                }
                ignored.insert((*g_trees[a].gene_tree.begin()).index);

                //insert children
                for(tree<PhyNode>::pre_order_iterator c=g_trees[a].gene_tree.begin(b);c!=g_trees[a].gene_tree.end(b);c++) {
                    ignored.insert((*c).index);
                }
            }
        }

        if (temp_vec.size() == 0) { //output the whole tree
            new_clusters.push_back(g_trees[a]);
        } else {    //output the rest clades
//            for(tree<PhyNode>::post_order_iterator b = g_trees[a].gene_tree.begin_post(); b != g_trees[a].gene_tree.end_post(); b++) {
//                if(ignored.count((*b).index)==0) {
//                    tree<PhyNode>::iterator it=g_trees[a].gene_tree.parent(b);
//                    //add this branch only when its parent is already output
//                    if(ignored.count((*it).index)>0) {
//                        QPCluster qc;
//                        qc.tree_id = g_trees[a].tree_id;
//                        qc.tree_file = g_trees[a].tree_file;
//                        qc.top_phy_index = (*b).phy_index;
//                        qc.gene_tree.insert_subtree(qc.gene_tree.begin(), b);
//                        qc.species_num=0;
//                        qc.is_true_tree=true;
//                        qc.save=true;
//
//                        for(tree<PhyNode>::leaf_iterator leaf_it=qc.gene_tree.begin_leaf();leaf_it!=qc.gene_tree.end_leaf();leaf_it++) qc.gene_ids.push_back((*leaf_it).name);
//                        temp_vec.push_back(qc);
////                        cerr<<"add"<<"\t"<<(*b).name<<endl;
//                    }
//                }
//            }
//            cout<<"XXXXXXXXXXXXX"<<g_trees[a].tree_id<<"\t"<<temp_vec.size()<<endl;
            if(temp_vec.size()>1) {
                for (long b = 0; b < temp_vec.size(); b++) {
                    stringstream suffix;
                    suffix << "_" << (b + 1);
                    temp_vec[b].tree_id += suffix.str();
                    temp_vec[b].tree_file += suffix.str();
                }
            }

            for(long b=0;b<temp_vec.size();b++) {
                new_clusters.push_back(temp_vec[b]);
            }
        }
    }
//    cerr<<"num_tree="<<new_clusters.size()<<"\t"<<g_trees.size()<<endl;
    g_trees.swap(new_clusters);
}

void Tree2GD::addExtraRoot() {
    cerr<<"add extra root from blast results"<<endl;
    map<string, vector<ParserLine> > gene2parsers;
    readBlastParser(PARSER_FILE, gene2parsers);

    for (long i = 0; i < g_trees.size(); i++) {
//        cerr<<g_trees[i].tree_id<<": "<<g_trees[i].top_phy_index<<"\t"<<(*phy_tree.begin()).phy_index<<endl;
        if (g_trees[i].og_ids.size()>0) continue;

        set<string> gene_set;
        for (long j = 0; j < g_trees[i].gene_ids.size(); j++) gene_set.insert(g_trees[i].gene_ids[j]);

        double max_score = 0;
        string target_id = "";

//        cerr<<"add root for "<<g_trees[i].tree_id<<endl;
        for (long j = 0; j < g_trees[i].gene_ids.size(); j++) {
//            cerr<<"\t"<<j<<": "<<g_trees[i].gene_ids[j]<<"\t"<<gene2parsers.count(g_trees[i].gene_ids[j])<<endl;
            if (gene2parsers.count(g_trees[i].gene_ids[j]) == 0) continue;
            for (long k = 0; k < gene2parsers[g_trees[i].gene_ids[j]].size(); k++) {
                //find a target not in this gene list
                if (gene_set.count(gene2parsers[g_trees[i].gene_ids[j]][k].target_id) == 0) {
                    double score = gene2parsers[g_trees[i].gene_ids[j]][k].bit_score;
                    string id = gene2parsers[g_trees[i].gene_ids[j]][k].target_id;
                    if (max_score < score) {
                        max_score = score;
                        target_id = id;
                    }
                }
            }
        }
//        cerr<<"\ttarget="<<target_id<<" score="<<max_score<<endl;

        if (max_score > 0) {
            g_trees[i].gene_ids.push_back(target_id);
            g_trees[i].og_ids.push_back(target_id);

            //add a new root
            PhyNode node1, node2, node3;
            initializeNode(node1);
            initializeNode(node2);
            initializeNode(node3);

            node1.name = "root_node";
            node2.name = target_id;
            node3.name = "temp";

            tree<PhyNode>::iterator ori_root = g_trees[i].gene_tree.begin();
            tree<PhyNode>::iterator it1 = g_trees[i].gene_tree.insert(g_trees[i].gene_tree.begin(), node1); //or use insert_after()
            tree<PhyNode>::iterator it2 = g_trees[i].gene_tree.append_child(it1, node2);
            tree<PhyNode>::iterator it3 = g_trees[i].gene_tree.append_child(it1, node3);

            g_trees[i].gene_tree.move_ontop(it3, ori_root);
        } else {
            cerr<<"\tno outgroup found for tree: "<<g_trees[i].tree_id<<endl;
        }
    }
}

void Tree2GD::setIndex(tree<PhyNode>& curr_tree) {
    long index = 0;
    for(tree<PhyNode>::post_order_iterator i = curr_tree.begin_post();i != curr_tree.end_post();i++) {
//        (*it1).alias=(*it1).name;
        (*i).index = index;
        index++;
    }
}

void Tree2GD::setPhyIndex(tree<PhyNode>& curr_tree) {
    for (tree<PhyNode>::post_order_iterator a = curr_tree.begin_post(); a != curr_tree.end_post(); a++) {
        if (a.number_of_children() == 0) continue;

        //find LCA
        long min_index = phy_tree.size();
        long max_index = -1;
        long temp = 0;

        for (tree<PhyNode>::leaf_iterator b = curr_tree.begin_leaf(a); b != curr_tree.end_leaf(a); b++) {
            temp = (*b).phy_index;
            if (min_index > temp) min_index = temp;
            if (max_index < temp) max_index = temp;
        }
        //            cout<<min_index<<"\t"<<max_index<<endl;
        tree<PhyNode>::iterator lca = getLCA(phy_tree, min_index, max_index);
        (*a).phy_index = (*lca).index;
    }
}

void Tree2GD::setMinKaKs4GDs() {
    for (long a = 0; a < gds.size(); a++) {
        map<string,vector<double> > species_ks;
//        vector<double> total_ks;
        for(long b=0;b<gds[a].gene_pairs.size();b++) {
            string s_id=gds[a].gene_pairs[b].species_id;
            string id1=gds[a].gene_pairs[b].gene1;
            string id2=gds[a].gene_pairs[b].gene2;
            if(id1>id2) {
                string s=id1;
                id1=id2;
                id2=s;
            }
            if(gene2omega.count(id1)==0 || gene2omega[id1].count(id2)==0) continue;

            if(species_ks.count(s_id)==0) {
                vector<double> vec;
                species_ks[s_id]=vec;
            }

            species_ks[s_id].push_back(gene2omega[id1][id2].ks);
//            total_ks.push_back(gene2omega[id1][id2].ks);
        }

        vector<double> total_ks;
        for(map<string,vector<double> >::iterator it=species_ks.begin();it!=species_ks.end();it++) {
            if(it->second.size()==0) continue;
            quickSortDouble(it->second, 0, it->second.size()-1, true);
            gds[a].species_ks[it->first] = it->second[0];
            total_ks.push_back(it->second[0]);
        }

        if(total_ks.size()==0) {
            gds[a].ks=-1;
        } else {
            quickSortDouble(total_ks, 0, total_ks.size()-1, true);
            gds[a].ks=quantile(total_ks, 0.5);
//            gds[a].ks=total_ks[0];
        }
    }
}

void Tree2GD::setMedianKaKs4GDs() {
    for (long a = 0; a < gds.size(); a++) {
        map<string,vector<double> > species_ks;
        vector<double> total_ks;
        for(long b=0;b<gds[a].gene_pairs.size();b++) {
            string s_id=gds[a].gene_pairs[b].species_id;
            string id1=gds[a].gene_pairs[b].gene1;
            string id2=gds[a].gene_pairs[b].gene2;
            if(id1>id2) {
                string s=id1;
                id1=id2;
                id2=s;
            }
            if(gene2omega.count(id1)==0 || gene2omega[id1].count(id2)==0) continue;

            if(species_ks.count(s_id)==0) {
                vector<double> vec;
                species_ks[s_id]=vec;
            }

            species_ks[s_id].push_back(gene2omega[id1][id2].ks);
            total_ks.push_back(gene2omega[id1][id2].ks);
        }

        for(map<string,vector<double> >::iterator it=species_ks.begin();it!=species_ks.end();it++) {
            if(it->second.size()==0) continue;
            quickSortDouble(it->second, 0, it->second.size()-1, true);
            gds[a].species_ks[it->first] = quantile(it->second, 0.5);
        }

        if(total_ks.size()==0) continue;
        quickSortDouble(total_ks, 0, total_ks.size()-1, true);
        gds[a].ks=quantile(total_ks, 0.5);
    }
}

void Tree2GD::adjustGDsByKs1() {
    vector<int> candidates;

    map<long, vector<double> > node2ks_counts;
    map<long, double> node2ks_median;
    map<long, double> node2ks_quantile05;
    map<long, double> node2ks_quantile95;
    for(tree<PhyNode>::pre_order_iterator it=phy_tree.begin();it!=phy_tree.end();it++) {
        vector<double> vec;
        node2ks_counts[(*it).phy_index]=vec;
        node2ks_median[(*it).phy_index]=-1;
        node2ks_quantile05[(*it).phy_index]=-1;
        node2ks_quantile95[(*it).phy_index]=-1;
    }

    //collect ks for each node, and classify gds without enough support (depth_var==0) into candidates
    for(long i=0;i<gds.size();i++) {
//        long index=gds[i].phy_index;
        if(gds[i].save && gds[i].depth_var==0 && gds[i].ks <= MAX_KS) {
            node2ks_counts[gds[i].phy_index].push_back(gds[i].ks);
//            cout<<(*phy_index2node[gds[i].phy_index]).name<<"\t"<<gds[i].median_ks<<endl;
        } else {
            candidates.push_back(i);
        }
    }

    for(map<long, vector<double> >::iterator it=node2ks_counts.begin();it!=node2ks_counts.end();it++) {
        if(it->second.size()<2) continue;
        quickSortDouble(it->second, 0, it->second.size()-1, true);
        node2ks_median[it->first]=quantile(it->second, 0.5);
        node2ks_quantile05[it->first]=quantile(it->second, 0.05);
        node2ks_quantile95[it->first]=quantile(it->second, 0.95);
    }

    for(long i=0;i<candidates.size();i++) {
        long index1=gds[candidates[i]].phy_index;
        long index2=gds[candidates[i]].overlap_lca_index;

        if(node2ks_median[index1]<0 || node2ks_median[index2]<0) continue;
        if(node2ks_median[index1] < node2ks_median[index2]) continue;

        double ks=gds[candidates[i]].ks;
        if(ks < node2ks_quantile05[index1] && ks < node2ks_quantile95[index2]) {
            gds[candidates[i]].phy_index = index2;
            gds[candidates[i]].comment = (*phy_index2node[index1]).name;
        }
    }
}

void Tree2GD::adjustGDsByKs2() {
    vector<int> candidates;

    map<long, vector<double> > node2ks_counts;
    map<long, double> node2ks_median;
    for(tree<PhyNode>::pre_order_iterator it=phy_tree.begin();it!=phy_tree.end();it++) {
        vector<double> vec;
        node2ks_counts[(*it).phy_index]=vec;
        node2ks_median[(*it).phy_index]=-1;
    }

    //collect ks for each node, and classify gds without enough support (depth_var>0) into candidates
    for(long i=0;i<gds.size();i++) {
        if(!gds[i].save) continue;

        if(gds[i].depth_var==0) {
            if(gds[i].ks>=0 && gds[i].ks <= MAX_KS) node2ks_counts[gds[i].phy_index].push_back(gds[i].ks);
        } else {
            if(gds[i].phy_index<=gds[i].overlap_lca_index) cerr<<"ERROR: "<<i<<", "<<gds[i].phy_index<<","<<gds[i].overlap_lca_index<<endl;
            candidates.push_back(i);
        }
    }

    for(map<long, vector<double> >::iterator it=node2ks_counts.begin();it!=node2ks_counts.end();it++) {
        if(it->second.size()<2) continue;
        quickSortDouble(it->second, 0, it->second.size()-1, true);
        node2ks_median[it->first]=quantile(it->second, 0.5);
        if(PRINT) cout<<">>>"<<(*phy_index2node[it->first]).name<<"\t"<<quantile(it->second, 0)<<"\t"<<quantile(it->second, 0.25)<<"\t"<<quantile(it->second, 0.5)<<"\t"<<quantile(it->second, 0.75)<<"\t"<<quantile(it->second, 1.0)<<endl;
    }

    map<long, map<long, double> > cutoffs;
    for(long i=0;i<candidates.size();i++) {
        long index1=gds[candidates[i]].phy_index;
        long index2=gds[candidates[i]].overlap_lca_index;

        if(node2ks_counts[index1].size()==0 || node2ks_counts[index2].size()==0) continue;
        if(node2ks_median[index1]<0 || node2ks_median[index2]<0) continue;
        if(node2ks_median[index1] < node2ks_median[index2]) continue;

        if(cutoffs.count(index1)==0) {
            map<long, double> map1;
            map1[index2]=-1;
            cutoffs[index1]=map1;
        }
        if(cutoffs[index1].count(index2)==0)  cutoffs[index1][index2]=-1;
    }

//    bool print=false;
    for(map<long, map<long, double> >::iterator it1=cutoffs.begin();it1!=cutoffs.end();it1++) {
        for(map<long, double>::iterator it2=it1->second.begin();it2!=it1->second.end();it2++) {
            long index1 = it1->first;
            long index2 = it2->first;
//            if(index1>=10 && index1<=16 && index2>=10 && index2<=16) print=true;
//            else print=false;

            long direc = 1;
            double current = (node2ks_median[index1] * node2ks_counts[index2].size() + node2ks_median[index2] * node2ks_counts[index1].size()); //index: 1*2 + 2*1
            current /= (node2ks_counts[index1].size() + node2ks_counts[index2].size());

            double bias1 = binarySearchDouble(node2ks_counts[index1], current);
            double bias2 = node2ks_counts[index2].size() - binarySearchDouble(node2ks_counts[index2], current);
            if (bias1 - bias2 < 0) direc = 1;
            else direc = -1;

//            if(print) cout<<"index1="<<index1<<" "<<node2ks_counts[index1].size()<<" "<<node2ks_median[index1]<<endl;
//            if(print) cout<<"index2="<<index2<<" "<<node2ks_counts[index2].size()<<" "<<node2ks_median[index2]<<endl;
//            if(print) cout<<"current="<<current<<"\tbias1="<<bias1<<"\tbias2="<<bias2<<endl;

            if(PRINT) cout<<(*phy_index2node[index1]).name<<","<<(*phy_index2node[index2]).name<<"\t"<<current<<","<<direc<<" "<<bias1<<","<<bias2<<endl;
            double step = 0.01;
            current += step*direc;
            while ((bias1 - bias2) * direc < 0) {
                bias1 = binarySearchDouble(node2ks_counts[index1], current);
                bias2 = node2ks_counts[index2].size() - binarySearchDouble(node2ks_counts[index2], current);
                current += step*direc;
//                if(print) cout<<"\t"<<current<<","<<direc<<" "<<bias1<<","<<bias2<<endl;
//                if(current>node2ks_median[index1] || current<node2ks_median[index2]) break;
                if(current>node2ks_median[index1]) break;
            }
            cutoffs[index1][index2] = current;
        }
    }

    for(long i=0;i<candidates.size();i++) {
        long index1=gds[candidates[i]].phy_index;
        long index2=gds[candidates[i]].overlap_lca_index;

        if(cutoffs.count(index1)==0 || cutoffs[index1].count(index2)==0 || cutoffs[index1][index2]<0) continue;

        if(gds[candidates[i]].ks < cutoffs[index1][index2]) {
            gds[candidates[i]].phy_index = index2;
            gds[candidates[i]].comment = (*phy_index2node[index1]).name;
        }
    }
}

void Tree2GD::deleteNodes(tree<PhyNode>& curr_tree, vector<tree<PhyNode>::iterator>& nodes) {
//    printTree(stdout,curr_tree,0);
    if(nodes.size()==0) return;

    //remove selected nodes
    for(long i=0;i<nodes.size();i++) {
        if(nodes[i]==curr_tree.begin()) continue;
        curr_tree.erase(nodes[i]);
    }

    //remove internal nodes without genes (in case of both two genes are removed)
    for (tree<PhyNode>::post_order_iterator a = curr_tree.begin_post(); a != curr_tree.end_post();) {
        if (a.number_of_children()==0 && !(*a).is_leaf) {
//            cout<<"internal: "<<(*a).name<<endl;
            curr_tree.erase(a++);
        }
        else a++;
    }

    //remove nodes with a single child
    for (tree<PhyNode>::pre_order_iterator a = curr_tree.begin(); a != curr_tree.end();) {
        if (a.number_of_children() == 1) {
            tree<PhyNode> sub_tree = curr_tree.subtree(a.begin(), a.end());
            a = curr_tree.move_ontop(a, sub_tree.begin());
        } else a++;
    }
}

void Tree2GD::readGene2SpeciesMap(string in_name, map<string,string> & id_map) {
    cerr<<"load idmap: "<<in_name<<endl;

    ifstream is;
    is.open(in_name.c_str(), ios::in);
    if (is.fail()) {
        fprintf(stderr, "The file %s does not exist!\n", in_name.c_str());
        is.close();
        exit(0);
    }

    set<string> species;
    string line="";
    while (getline(is, line, '\n')) {
        if(line.length()==0) continue;
        StringTokenizer nizer(line, "\t");
        if (nizer.size() != 2) continue;
        //format: gene_id species_id
        id_map[nizer.getAt(0)]=nizer.getAt(1);
        species.insert(nizer.getAt(1));
    }
    is.close();

    if(id_map.size()<species.size()) {
        fprintf(stderr,"gene number is less than species number, please check\n");
        exit(0);
    }
    cerr<<id_map.size()<<" genes loaded for "<<species.size()<<" species"<<endl;
}

void Tree2GD::readTreeList(string in_name, vector<QPCluster> & g_trees) {
    cerr<<"load tree list: "<<in_name<<endl;
    ifstream is;
    is.open(in_name.c_str(), ios::in);
    if (is.fail()) {
        fprintf(stderr, "The file %s does not exist!\n", in_name.c_str());
        is.close();
        exit(0);
    }

    string line="";
    while (getline(is, line, '\n')) {
        StringTokenizer nizer(line, "\t");
        if (nizer.size() < 2) {
            fprintf(stderr, "ignoring: %s\n", line.c_str());
            continue;
        }
        QPCluster qc;
        qc.tree_id=nizer.getAt(0);
        qc.tree_file=nizer.getAt(1);
        qc.top_phy_index=-1;
        qc.species_num=0;
        qc.is_true_tree=true;
        qc.save=true;

        g_trees.push_back(qc);
    }
    is.close();
    cerr<<"\tsize="<<g_trees.size()<<endl;
}

void Tree2GD::readNewickTree(string in_name, tree<PhyNode> & curr_tree, vector<tree<PhyNode>::iterator> & nodes, vector<tree<PhyNode>::iterator> & leaves, string prefix) {
    //    cerr<<"load tree: "<<in_name<<endl;
    ifstream is;
    is.open(in_name.c_str(), ios::in);
    if (is.fail()) {
        fprintf(stderr, "The file %s does not exist!\n", in_name.c_str());
        is.close();
        exit(0);
    }

    string contents="";
    string line="";
    while (getline(is, line, '\n')) {
        contents+=line;
    }

    vector<long> stack;
    long id=0;

    vector<PhyNode> init_nodes;
    map<long,long> node2parent;

    long i=0;
    while(i<contents.length()) {
//        cout<<contents[i]<<endl;
        if(contents[i]=='(') {
            i++;
            continue;
        } else if(contents[i]==')') {
            //in case of extra "()" are used, e.g. ((A,B))
            if(stack.size()<2) continue;
            //popup the last two elements
//            for(long a=0;a<stack.size();a++) cout<<"\t"<<init_nodes[stack[a]].name<<endl;
            long prev1=stack[stack.size()-1];
            stack.pop_back();
            long prev2=stack[stack.size()-1];
            stack.pop_back();

            node2parent[prev1]=init_nodes.size();
            node2parent[prev2]=init_nodes.size();

            stringstream ss;
            ss<<prefix<<"_"<<id;
            id++;

            PhyNode node;
            initializeNode(node);
            node.name=ss.str();
//            if(node.name.find_first_of("|")!=string::npos) node.name.erase(node.name.find_first_of("|"));
            node.dist=0;

            stack.push_back(init_nodes.size());
            init_nodes.push_back(node);
//            cout<<init_nodes[prev1].name<<" & "<<init_nodes[prev2].name<<" -> "<<node.name<<" size="<<stack.size()<<endl;
            //read bootstrap value if have
            i++;
            string value="";
            for(;i<contents.length();i++) {
                if(contents[i]!='.' && (contents[i]>'9' || contents[i]<'0')) {
                    i--;
                    break;
                }
                value+=contents[i];
            }
//            cout<<"value="<<value<<endl;
            double bootstrap=0;
            if(value.length()>0) sscanf(value.c_str(),"%lf",&bootstrap);
            init_nodes[stack[stack.size()-1]].bootstrap=bootstrap;
        } else if(contents[i]==':') {
            i++;
            string value="";
            for(;i<contents.length();i++) {
                if(contents[i]!='.' && (contents[i]>'9' || contents[i]<'0')) {
                    i--;
                    break;
                }
                value+=contents[i];
            }
//            cout<<"value="<<value<<endl;
            double dist=0;
            if(value.length()>0) sscanf(value.c_str(),"%lf",&dist);
            init_nodes[stack[stack.size()-1]].dist=dist;
        } else if(contents[i]==',') {
            i++;
            continue;
        } else if(contents[i]==';') {
            break;
        } else {
            //read taxon name
            string name="";
            for(;i<contents.length();i++) {
                if(contents[i]=='(' || contents[i]==')' || contents[i]==':' || contents[i]==',' || contents[i]==';') {
                    i--;
                    break;
                }
                name+=contents[i];
            }
            PhyNode node;
            initializeNode(node);
            node.name=name;
            node.dist=0;
            node.bootstrap=100;
//            cout<<"----"<<node.name<<" "<<node.dist<<endl;
            stack.push_back(init_nodes.size());
            init_nodes.push_back(node);
        }
        i++;
    }
//    cout<<stack.size()<<endl;

    //for unrooted tree, within (A,B,C), B and C was already grouped as prev1, while A is prev2
//    fprintf(stderr, "stack size=%ld\n", stack.size());
    if(stack.size()>1) {
        long prev1 = stack[stack.size() - 1];
        stack.pop_back();
        long prev2 = stack[stack.size() - 1];
        stack.pop_back();

        //dist of prev2 was equaly assigned to prev1 and prev2
        //not needed, they will be updated in reRoot();
//        init_nodes[prev2].dist/=2;
//        init_nodes[prev1].dist=init_nodes[prev2].dist;

        //assign bootstrap value of prev2 to prev1
        init_nodes[prev1].bootstrap=init_nodes[prev2].bootstrap;

        node2parent[prev1] = init_nodes.size();
        node2parent[prev2] = init_nodes.size();

        stringstream ss;
        ss << prefix << "_" << id;
        id++;

        PhyNode node;
        initializeNode(node);
        node.name = ss.str();
        node.dist = 0;
        node.bootstrap=100;

        stack.push_back(init_nodes.size());
        init_nodes.push_back(node);
    }

    set<long> parents;
    long root_index = init_nodes.size() - 1;
    for (long b = 0; b < init_nodes.size(); b++) {
        if (node2parent.count(b) == 0) {
            root_index = b;
        } else {
            if(parents.count(node2parent[b])==0) parents.insert(node2parent[b]);
//            cout<<"add: "<<node2parent[b]<<endl;
        }
    }
    node2parent[root_index]=root_index;
//    fprintf(stderr, "root_index=%ld\n", root_index);
    if (root_index < 0) {
        fprintf(stderr, "error[15]: no root found.\n");
        exit(0);
    }

    map<long, tree<PhyNode>::iterator> saved;

    tree<PhyNode>::iterator root_it = curr_tree.insert(curr_tree.begin(), init_nodes[root_index]);
    saved[root_index] = root_it;

    for (long i = 0; i < init_nodes.size(); i++) {
        if (parents.count(i) > 0) continue;     //not a leaf
//        if (parents.count(init_nodes[i].taxa_id) > 0) continue;
//        cout<<i<<": "<<init_nodes[i].name<<endl;
        if (node2parent.count(i) == 0) {
            fprintf(stderr, "error[8] (not parent found): %s\n", init_nodes[i].name.c_str());
            continue;
        }
        //        leaves[i].rank=taxaid2rank[taxa_id];
        long this_id=i;
        long parent_id = node2parent[i];

        vector<long> lineage;
        while (this_id != parent_id) {
            lineage.push_back(this_id);
            this_id = parent_id;
            if (node2parent.count(this_id) == 0) break;
            parent_id = node2parent[this_id];
        }
//        cout<<"  deepth="<<lineage.size()<<endl;

        tree<PhyNode>::iterator parent_it = curr_tree.begin();
        for (long j = lineage.size() - 1; j >= 1; j--) {
//            cout<<"  "<<j<<": "<<lineage[j]<<endl;
            if (saved.count(lineage[j]) == 0) {
                parent_it = curr_tree.append_child(parent_it, init_nodes[lineage[j]]);
                saved[lineage[j]] = parent_it;
            } else {
                parent_it = saved[lineage[j]];
            }
        }

        tree<PhyNode>::iterator leaf_it = curr_tree.append_child(parent_it, init_nodes[i]);
        (*leaf_it).is_leaf = true;
        leaves.push_back(leaf_it);
        //        cout<<"  nodes="<<nc_tree.size()<<endl;
    }

    setIndex(curr_tree);
    is.close();
}

void Tree2GD::readQuickParanoid(string in_name, vector<QPCluster> & clusters,string prefix) {
    cerr<<"load quickparanoid file: "<<in_name<<endl;
    ifstream is;
    is.open(in_name.c_str(), ios::in);
    if (is.fail()) {
        fprintf(stderr, "The file %s does not exist!\n", in_name.c_str());
        is.close();
        exit(0);
    }

    string line="";

    //read first line
    if (!getline(is, line, '\n')) {
        is.close();
        return;
    }
    //read contents
    set<string> ignored;
    for(long i=0;i<g_trees.size();i++) ignored.insert(g_trees[i].tree_id);
    map<string, long> id2index;
    while (getline(is, line, '\n')) {
        StringTokenizer nizer(line, "\t");
        if (nizer.size() < 7) continue;
        if(ignored.count(nizer.getAt(0))>0) continue;

        if(id2index.count(nizer.getAt(0))==0) {
            QPCluster qc;
            qc.tree_id=nizer.getAt(0);
            qc.tree_file="unclustered_"+qc.tree_id+".raxml";
            qc.top_phy_index=-1;
            qc.gene_ids.push_back(nizer.getAt(2));
            qc.species_num=0;
            qc.is_true_tree=false;
            qc.save=true;

            if(gene_idmap.count(nizer.getAt(2))==0) {
                fprintf(stderr, "error[3], gene not found in the species map: %s\n", nizer.getAt(2).c_str());
                continue;
            }

            id2index[qc.tree_id]=clusters.size();
            clusters.push_back(qc);
        } else clusters[id2index[nizer.getAt(0)]].gene_ids.push_back(nizer.getAt(2));
    }
    is.close();

    //build pseudo trees for these cluster
    for(long i=0;i<clusters.size();i++) {
//        cout<<clusters[i].tree_id<<endl;
        //count specie set
        map<string, vector<string> > species_map;
        for(long j=0;j<clusters[i].gene_ids.size();j++) {
            string s_id=gene_idmap[clusters[i].gene_ids[j]];
            if(species_map.count(s_id)==0) {
                vector<string> vec;
                species_map[s_id]=vec;
            }
            species_map[s_id].push_back(clusters[i].gene_ids[j]);
//            cout<<"\t"<<clusters[i].gene_ids[j]<<"\t"<<s_id<<endl;
        }
        //clone a new tree
        tree<PhyNode> c_tree=phy_tree.subtree(phy_tree.begin(),phy_tree.end());
        //remove nodes not necessary
        set<long> visited;
        visited.insert((*c_tree.begin()).index);
        for(tree<PhyNode>::leaf_iterator a=c_tree.begin_leaf();a!=c_tree.end_leaf();a++) {
            if(species_map.count((*a).name)==0) continue;
            for(tree<PhyNode>::iterator b=a;b!=c_tree.begin();b=c_tree.parent(b)) {
                visited.insert((*b).index);
//                cout<<(*b).index<<"\t";
            }
//            cout<<endl;
        }
        //1st round, remove nodes without genes
        for(tree<PhyNode>::post_order_iterator a=c_tree.begin_post();a!=c_tree.end_post();) {
//            cout<<"++"<<(*a).index<<"\t"<<visited.count((*a).index)<<endl;
            if(visited.count((*a).index)==0) c_tree.erase(a++);
            else a++;
        }

        for(tree<PhyNode>::pre_order_iterator a=c_tree.begin();a!=c_tree.end();a++) {
            if(a.number_of_children()==1) {
                tree<PhyNode> sub_tree=c_tree.subtree(a.begin(),a.end());
                a=c_tree.move_ontop(a,sub_tree.begin());
            }
        }
//        printTree(stdout,c_tree,0);

        //add nodes for multiple-gene species
        for(tree<PhyNode>::leaf_iterator a=c_tree.begin_leaf();a!=c_tree.end_leaf();a++) {
            if(species_map[(*a).name].size()==0) continue;
//            cout<<(*a).name<<"\t"<<species_map[(*a).name].size()<<endl;

            for(long b=0;b<species_map[(*a).name].size();b++) {
                PhyNode node;
                initializeNode(node);
//                cloneNode((*a),node);
                node.name=species_map[(*a).name][b];
//                cout<<"\t--------"<<node.name<<endl;
                c_tree.insert(a.begin(),node);
            }
        }
//        printTree(stdout,c_tree,0);

        //2nd round, remove nodes with a single child
        for(tree<PhyNode>::pre_order_iterator a=c_tree.begin();a!=c_tree.end();) {
//            cout<<"set "<<(*a).name<<"\t"<<a.number_of_children()<<endl;
//            printTree(stdout,c_tree,0);
            if(a.number_of_children()==1) {
                tree<PhyNode> sub_tree=c_tree.subtree(a.begin(),a.end());
                a=c_tree.move_ontop(a,sub_tree.begin());
            } else a++;
//            printTree(stdout,c_tree,0);
        }
//        printTree(stdout,c_tree,0);

        //reset name and index
        long id=0;
        for(tree<PhyNode>::post_order_iterator a=c_tree.begin_post();a!=c_tree.end_post();a++) {
            if(a.number_of_children()>0) {
                (*a).is_leaf=false;
                stringstream ss;
                ss << prefix << "_" << id;
                (*a).name=ss.str();
                id++;
            } else (*a).is_leaf=true;
        }
        setIndex(c_tree);
//        printTree(stdout,c_tree,0);
        clusters[i].gene_tree=c_tree;
    }
    cerr<<"\t"<<clusters.size()<<" clusters added"<<endl;
}

void Tree2GD::readOmega(string in_name, map<string, map<string,Omega> > & omega_map) {
    cerr<<"load ka/ks/omega: "<<in_name<<endl;
    ifstream is;
    is.open(in_name.c_str(), ios::in);
    if (is.fail()) {
        fprintf(stderr, "The file %s does not exist!\n", in_name.c_str());
        is.close();
        exit(0);
    }

    long num=0;
    string line="";
    while (getline(is, line, '\n')) {
        num++;
        StringTokenizer nizer(line, "\t");
        if (nizer.size() < 5) {
            fprintf(stderr, "ignoring: %s\n", line.c_str());
            continue;
        }
        Omega om;

        string id1=nizer.getAt(0);
        string id2=nizer.getAt(1);
        if(id1>id2) {
            string s=id1;
            id1=id2;
            id2=s;
        }

        sscanf(nizer.getAt(2).c_str(), "%lf", &om.ka);
        sscanf(nizer.getAt(3).c_str(), "%lf", &om.ks);
        sscanf(nizer.getAt(4).c_str(), "%lf", &om.omega);

        if(omega_map.count(id1)==0) {
            map<string,Omega> map1;
            omega_map[id1]=map1;
        }
        if(omega_map[id1].count(id2)==0) {
            omega_map[id1][id2]=om;
        } else {
            cerr<<"ignore repeated records["<<num<<"]: "<<line<<endl;
        }
    }
    is.close();
    cerr<<"\tsize="<<num<<endl;
}

void Tree2GD::readBlastParser(string in_name, map<string,vector<ParserLine> > & gene2parsers) {
    cerr<<"load blast parser file: "<<in_name<<endl;
    ifstream is;
    is.open(in_name.c_str(), ios::in);
    if (is.fail()) {
        fprintf(stderr, "The file %s does not exist!\n", in_name.c_str());
        is.close();
        exit(0);
    }

    long num=0;
    string line="";

    while (getline(is, line, '\n')) {
        StringTokenizer nizer(line, "\t");
        if (nizer.size() < 10) {
//            cerr<<nizer.size()<<":\t"<<line<<endl;
            continue;
        }
        ParserLine p;
        p.query_id=nizer.getAt(0);
        p.target_id=nizer.getAt(1);
        sscanf(nizer.getAt(2).c_str(), "%lf", &p.bit_score);
        sscanf(nizer.getAt(3).c_str(), "%ld", &p.query_len);
        sscanf(nizer.getAt(4).c_str(), "%ld", &p.target_len);
        sscanf(nizer.getAt(5).c_str(), "%ld", &p.query_longest_match);
        sscanf(nizer.getAt(6).c_str(), "%ld", &p.target_longest_match);
        sscanf(nizer.getAt(7).c_str(), "%ld", &p.query_total_match);
        sscanf(nizer.getAt(8).c_str(), "%ld", &p.target_total_match);

        if(gene2parsers.count(p.query_id)==0) {
            vector<ParserLine> vec;
            gene2parsers[p.query_id]=vec;
        }
        gene2parsers[p.query_id].push_back(p);
        num++;
    }
    is.close();
    cerr<<"\t"<<num<<" blast hits loaded"<<endl;
}

void Tree2GD::readGenomeList(string in_name, set<string> & g_set) {
    cerr<<"load genome list: "<<in_name<<endl;
    ifstream is;
    is.open(in_name.c_str(), ios::in);
    if (is.fail()) {
        fprintf(stderr, "The file %s does not exist!\n", in_name.c_str());
        is.close();
        exit(0);
    }

    string line="";
    while (getline(is, line, '\n')) {
        StringTokenizer nizer(line, " \t");
        if (nizer.size() < 1) {
            fprintf(stderr, "ignoring: %s\n", line.c_str());
            continue;
        }

        g_set.insert(nizer.getAt(0));
    }
    is.close();
    cerr<<"\tsize="<<g_set.size()<<endl;
}

void Tree2GD::writePhTrees(string out_name){//cdy_add
  cerr<<"-> "<<out_name<<endl;
  ofstream os;
  os.open(out_name.c_str(), ios::out);
  if (os.fail()) {
      fprintf(stderr, "Can NOT open file for output: %s\n", out_name.c_str());
      return;
  }
  writeNewickTree(os,phy_tree,phy_tree.begin(),2);
  os.close();
}



void Tree2GD::readIgnoredIsoforms(string in_name, set<string> & isoform_set) {
    cerr<<"load isoform list: "<<in_name<<endl;
    ifstream is;
    is.open(in_name.c_str(), ios::in);
    if (is.fail()) {
        fprintf(stderr, "The file %s does not exist!\n", in_name.c_str());
        is.close();
        exit(0);
    }

    long total=0;
    string line="";
    while (getline(is, line, '\n')) {
        StringTokenizer nizer(line, " \t");
        if (nizer.size() < 4) {
            fprintf(stderr, "ignoring: %s\n", line.c_str());
            continue;
        }

        if(nizer.getAt(3)=="isoforms") isoform_set.insert(nizer.getAt(1));
        total++;
    }
    is.close();
    cerr<<"\tsize="<<isoform_set.size()<<endl;
}

void Tree2GD::writeSummary(string out_name) {
    cerr<<"-> "<<out_name<<endl;
    FILE * fp = fopen(out_name.c_str(),"w");
    fprintf(fp,"#species_tree\n");
    printTree(fp,phy_tree,1);
    for (long a = 0; a < g_trees.size(); a++) {
        if(!g_trees[a].save) continue;
        fprintf(fp,"#gene_tree: %s\t%s\n",g_trees[a].tree_id.c_str(),g_trees[a].tree_file.c_str());
        printTree(fp,g_trees[a].gene_tree,2);
    }
    fclose(fp);
}

void Tree2GD::writeGenePairs4GD(string out_name) {
    cerr<<"-> "<<out_name<<endl;
    ofstream os;
    os.open(out_name.c_str(), ios::out);
    if (os.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", out_name.c_str());
        return;
    }
    os<<"#cluster_id\tgd_id\tlevel\tspecies\tgene1\tgene2\tcomment"<<endl;
    for (long a = 0; a < gds.size(); a++) {
        if(!gds[a].save) continue;
        for (long b = 0; b < gds[a].gene_pairs.size(); b++) {
            os << gds[a].gene_tree_id;
            os << "\t" << (gds[a].gd_id+1);
//            os << "\t" << gds[a].node_name;
            os << "\t" << (*phy_index2node[gds[a].phy_index]).name;
            os << "\t" << gds[a].gene_pairs[b].species_id;
            os << "\t" << gds[a].gene_pairs[b].gene1;
            os << "\t" << gds[a].gene_pairs[b].gene2;
            os << "\t" << gds[a].comment;
            os << endl;
        }
    }
    os.close();
}

void Tree2GD::writeGenePairs4Ortholog(string out_name) {
    cerr<<"-> "<<out_name<<endl;

    map<string, set<string> > gd_map;
    for (long a = 0; a < gds.size(); a++) {
        if(!gds[a].save) continue;
        if(gd_map.count(gds[a].gene_tree_id)==0) {
            set<string> temp;
            gd_map[gds[a].gene_tree_id]=temp;
        }
        gd_map[gds[a].gene_tree_id].insert((*gds[a].gene_tree_node).name);
    }

    FILE * fp = fopen(out_name.c_str(),"w");
    for (long a = 0; a < g_trees.size(); a++) {
        if(!g_trees[a].save) continue;
        fprintf(fp,"#gene_tree: %s\t%s\n",g_trees[a].tree_id.c_str(),g_trees[a].tree_file.c_str());
//        printTree(fp1,g_trees[a].gene_tree,0);

        for (tree<PhyNode>::post_order_iterator b = g_trees[a].gene_tree.begin_post();b != g_trees[a].gene_tree.end_post();b++) {
//            fprintf(fp,">%s\t%d\n",(*b).name.c_str(),b.number_of_children());
            if(b.number_of_children()<2) {
                continue;
            }

            bool is_gd=false;
            if(gd_map.count(g_trees[a].tree_id)!=0 && gd_map[g_trees[a].tree_id].count((*b).name)!=0) is_gd=true;
//            fprintf(fp,"\t%d\n",is_gd);
            if(is_gd) continue;

            for (tree<PhyNode>::sibling_iterator c = b.begin(); c != b.end(); c++) {
                vector<string> vec0;
                if((*c).is_leaf) vec0.push_back((*c).name);
                else {
                    for (tree<PhyNode>::leaf_iterator w = g_trees[a].gene_tree.begin_leaf(c); w != g_trees[a].gene_tree.end_leaf(c); w++) {
                        if(ignore4ortholog.count((*w).name)==0) vec0.push_back((*w).name);
                    }
                }
                tree<PhyNode>::sibling_iterator d=c;
                d++;
                if(d==b.end()) continue;
                for (; d != b.end(); d++) {
//                    fprintf(fp,"\t%s\t%s\n",(*c).name.c_str(),(*d).name.c_str());
                    if(c==d) continue;

                    vector<string> vec1;
                    if ((*d).is_leaf) vec1.push_back((*d).name);
                    else {
                        for (tree<PhyNode>::leaf_iterator w = g_trees[a].gene_tree.begin_leaf(d); w != g_trees[a].gene_tree.end_leaf(d); w++) {
                            if(ignore4ortholog.count((*w).name)==0) vec1.push_back((*w).name);
                        }
                    }
                    for (long m=0;m<vec0.size(); m++) {
                        for (long n=0; n<vec1.size(); n++) {
                            if(gene_idmap[vec0[m]]==gene_idmap[vec1[n]]) continue;
                            fprintf(fp,"%s\t%s\n",vec0[m].c_str(),vec1[n].c_str());
                        }
                    }
                }
            }
        }
    }
    fclose(fp);
}

void Tree2GD::writeSingleGDPattern(string out_name) {
    cerr<<"-> "<<out_name<<endl;
    ofstream os;
    os.open(out_name.c_str(), ios::out);
    if (os.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", out_name.c_str());
        return;
    }
    os<<"#cluster_id\tgd_id\tlevel\tspecies\tpattern\tcomment"<<endl;

    for (long a = 0; a < gds.size(); a++) {
        if(!gds[a].save) continue;

        tree<PhyNode>::iterator node=phy_index2node[gds[a].phy_index];

        if(node.number_of_children()<2) {
            long num=0;
            if (gds[a].clade1.count((*node).phy_index) > 0) num++;
            if (gds[a].clade2.count((*node).phy_index) > 0) num++;

            os << gds[a].gene_tree_id;
            os << "\t" << (gds[a].gd_id + 1);
            os << "\t" << (*node).name;
            os << "\t" << (*node).name;
            os << "\t" << num;
            os << "\t" << gds[a].comment;
            os << endl;
        } else {
            for (tree<PhyNode>::iterator b = phy_tree.begin(node); b != phy_tree.end(node); b++) {
                long num=0;
                if (gds[a].clade1.count((*b).phy_index) > 0) num++;
                if (gds[a].clade2.count((*b).phy_index) > 0) num++;

                os << gds[a].gene_tree_id;
                os << "\t" << (gds[a].gd_id + 1);
                os << "\t" << (*node).name;
                os << "\t" << (*b).name;
                os << "\t" << num;
                os << "\t" << gds[a].comment;
                os << endl;
            }
        }


    }
    os.close();
}

void Tree2GD::writeSummarytable(string out_name) {//cdy_add
    cerr<<"-> "<<out_name<<endl;
    FILE * fp = fopen(out_name.c_str(),"w");
    fprintf(fp, "Newick_label\tphID\tGD\tNUM\tGDratio\n");
    printSummarytable(fp,phy_tree);
    fclose(fp);
}
void Tree2GD::printSummarytable(FILE* fp, tree<PhyNode>& sub_tree){//cdy_add

  map<long, long> branch_points;
  tree<PhyNode>::pre_order_iterator it = sub_tree.begin();
  while (it != sub_tree.end()){
    long depth = sub_tree.depth(it);
    if (it.number_of_children() > 1) branch_points[depth + 1] = it.number_of_children();
    fprintf(fp, "%s\t%ld\t%ld\t%ld\t%.2lf%s\n", (*it).name.c_str(), (*it).index, (*it).gd_count, (*it).lineage_count, (100.0 * (*it).gd_count / (*it).lineage_count),"%");
    it++;
  }
}

void Tree2GD::writeSingleGDLineage(string out_name) {
    cerr<<"-> "<<out_name<<endl;
    ofstream os;
    os.open(out_name.c_str(), ios::out);
    if (os.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", out_name.c_str());
        return;
    }
    os<<"#cluster_id\tgd_id\tlevel\tclade1\tclade2"<<endl;

    for (long a = 0; a < gds.size(); a++) {
        if(!gds[a].save) continue;

        tree<PhyNode>::iterator node=phy_index2node[gds[a].phy_index];

        os << gds[a].gene_tree_id;
        os << "\t" << (gds[a].gd_id + 1);
        os << "\t" << (*node).name;

        for(tree<PhyNode>::sibling_iterator b=gds[a].gene_tree_node.begin();b!=gds[a].gene_tree_node.end();b++) {
            //iterate all leaves although we use iterator
            string str;
            if(b.number_of_children()<2) {
                str += (*b).name;
            } else {
                for (tree<PhyNode>::iterator c = b.begin(); c != b.end(); c++) {    //post_order_iterator does NOT work when iterating subnodes
                    if (c.number_of_children() < 2) {
                        if (str.length() > 0) str += ",";
                        str += (*c).name;
                    }
                }
            }
            os<<"\t"<<str;
        }
        os << endl;
    }
    os.close();
}

void Tree2GD::writeAncestralGDRetention(string out_name) {
    cerr<<"-> "<<out_name<<endl;
    ofstream os;
    os.open(out_name.c_str(), ios::out);
    if (os.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", out_name.c_str());
        return;
    }
    os<<"#cluster_id\tgd_id\tlevel\tspecies1\tspecies2\tpattern1\tpattern2\tcomment"<<endl;

    //collect inherit relationship between phy_nodes
    map<long, set<long> > inherit;
    for(tree<PhyNode>::post_order_iterator a=phy_tree.begin_post();a!=phy_tree.end_post();a++) {
        set<long> set1;
        for(tree<PhyNode>::sibling_iterator b=a.begin();b!=a.end();b++) {
            for(set<long>::iterator c=inherit[(*b).phy_index].begin();c!=inherit[(*b).phy_index].end();c++) set1.insert(*c);
        }
        set1.insert((*a).phy_index);
        inherit[(*a).phy_index]=set1;
    }

    for (long a = 0; a < gds.size(); a++) {
        if(!gds[a].save) continue;

        tree<PhyNode>::iterator node=phy_index2node[gds[a].phy_index];

        for (tree<PhyNode>::iterator b = phy_tree.begin(node); b != phy_tree.end(node); b++) {
            for (tree<PhyNode>::iterator c = phy_tree.begin(node); c != phy_tree.end(node); c++) {
                if((*b).phy_index>=(*c).phy_index) continue;
                if(inherit[(*b).phy_index].count((*c).phy_index)>0 || inherit[(*c).phy_index].count((*b).phy_index)>0) continue;

                os << gds[a].gene_tree_id;
                os << "\t" << (gds[a].gd_id+1);
                os << "\t" << (*node).name;
                os << "\t" << (*b).name;
                os << "\t" << (*c).name;
                os << "\t" ;
                if(gds[a].clade1.count((*b).phy_index)>0) os << "1" ;
                else os << "0" ;
                if(gds[a].clade2.count((*b).phy_index)>0) os << "1" ;
                else os << "0" ;
                os << "\t" ;
                if(gds[a].clade1.count((*c).phy_index)>0) os << "1" ;
                else os << "0" ;
                if(gds[a].clade2.count((*c).phy_index)>0) os << "1" ;
                else os << "0" ;
                os << "\t" << gds[a].comment;
                os << endl;
            }
        }
//        for (tree<PhyNode>::leaf_iterator b = phy_tree.begin_leaf(node); b!=phy_tree.end_leaf(node);b++) {
//            for (tree<PhyNode>::leaf_iterator c = phy_tree.begin_leaf(node); c!=phy_tree.end_leaf(node);c++) {
//                if((*b).phy_index>=(*c).phy_index) continue;
//                os << gds[a].gene_tree_id;
//                os << "\t" << (gds[a].gd_id+1);
//                os << "\t" << (*node).name;
//                os << "\t" << (*b).name;
//                os << "\t" << (*c).name;
//                os << "\t" ;
//                if(gds[a].clade1.count((*b).phy_index)>0) os << "1" ;
//                else os << "0" ;
//                if(gds[a].clade2.count((*b).phy_index)>0) os << "1" ;
//                else os << "0" ;
//                os << "\t" ;
//                if(gds[a].clade1.count((*c).phy_index)>0) os << "1" ;
//                else os << "0" ;
//                if(gds[a].clade2.count((*c).phy_index)>0) os << "1" ;
//                else os << "0" ;
//                os << "\t" << gds[a].comment;
//                os << endl;
//            }
//        }
    }
    os.close();
}


void Tree2GD::writeGDtype(string out_name){//cdy_add
  cerr<<"-> "<<out_name<<endl;
  ofstream os;
  os.open(out_name.c_str(), ios::out);
  if (os.fail()) {
      fprintf(stderr, "Can NOT open file for output: %s\n", out_name.c_str());
      return;
  }
  os<<"gd_node\tAABB\tAXBB\tAABX"<<endl;
  //collect inherit relationship between phy_nodes
  map<long, set<long> > inherit;
  for(tree<PhyNode>::post_order_iterator a=phy_tree.begin_post();a!=phy_tree.end_post();a++) {
      set<long> set1;
      for(tree<PhyNode>::sibling_iterator b=a.begin();b!=a.end();b++) {
          for(set<long>::iterator c=inherit[(*b).phy_index].begin();c!=inherit[(*b).phy_index].end();c++) set1.insert(*c);
      }
      set1.insert((*a).phy_index);
      inherit[(*a).phy_index]=set1;
  }
      map<string,map<string,int> > gdtypemap;
  for (long a = 0; a < gds.size(); a++) {
      if(!gds[a].save) continue;

      tree<PhyNode>::iterator node=phy_index2node[gds[a].phy_index];
      tree<PhyNode>::iterator b = phy_tree.begin(node);



      if(b != phy_tree.end(node)){
        if(gdtypemap.count((*node).name)==0){
         gdtypemap[(*node).name]["AABB"]=0;
         gdtypemap[(*node).name]["AXBB"]=0;
         gdtypemap[(*node).name]["AABX"]=0;}
        tree<PhyNode>::iterator c = b;
        c++;
        while(inherit[(*b).phy_index].count((*c).phy_index)>0 || inherit[(*c).phy_index].count((*b).phy_index)>0) c++;
        string gdtype;
        if(gds[a].clade1.count((*b).phy_index)>0) gdtype.append("A") ;
        else gdtype.append("X") ;
        if(gds[a].clade2.count((*b).phy_index)>0) gdtype.append("A") ;
        else gdtype.append("X") ;
        if(gds[a].clade1.count((*c).phy_index)>0) gdtype.append("B") ;
        else gdtype.append("X") ;
        if(gds[a].clade2.count((*c).phy_index)>0) gdtype.append("B") ;
        else gdtype.append("X") ;
        if(gdtype=="AABB") gdtypemap[(*node).name]["AABB"]+=1;
        if(gdtype=="AXBB"||gdtype=="XABB") gdtypemap[(*node).name]["AXBB"]+=1;
        if(gdtype=="AABX"||gdtype=="AAXB") gdtypemap[(*node).name]["AABX"]+=1;
      } else {continue;}
}
      map<string,map<string,int> >::iterator n=gdtypemap.begin();
      while(n!=gdtypemap.end()){
        os<<n->first<<"\t"<<n->second["AABB"]<<"\t"<<n->second["AXBB"]<<"\t"<<n->second["AABX"]<<endl;
        n++;
      }
}


void Tree2GD::writeRecentGDRetention(string out_name) {
    cerr<<"-> "<<out_name<<endl;
    ofstream os;
    os.open(out_name.c_str(), ios::out);
    if (os.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", out_name.c_str());
        return;
    }
    os<<"#cluster_id\tgd_id\tchild1\tchild2\tlevel\trecent_level\ttype"<<endl;
    for (long a = 0; a < gds.size(); a++) {
        if(!gds[a].save) continue;

        map<long, long> phy2child_gd1;
        map<long, long> phy2child_gd2;
//        cout<<(gds[a].gd_id+1)<<"\t"<<gds[a].child_gd1.size()<<"\t"<<gds[a].child_gd2.size()<<endl;

        //child.bootstrap doesn't have to be over than MIN_BOOTSTRAP (that means child.save could be false)
        for(long b=0;b<gds[a].child_gd1.size();b++) {
            long index=gds[a].child_gd1[b];
            phy2child_gd1[gds[index].phy_index]=index;
//            cout<<" ."<<(*phy_index2node[gds[index].phy_index]).name<<" "<<index<<endl;
        }
        for(long b=0;b<gds[a].child_gd2.size();b++) {
            long index=gds[a].child_gd2[b];
            phy2child_gd2[gds[index].phy_index]=index;
//            cout<<" :"<<(*phy_index2node[gds[index].phy_index]).name<<" "<<index<<endl;
        }

        //1=((G,_),(_,_))
        //2=((G,_),(G,_))
        //3=((G,G),(_,_))
        //4=((G,G),(G,_))
        //5=((G,G),(G,G))
        tree<PhyNode>::iterator it=phy_index2node[gds[a].phy_index];

        long type = 0;
        if (phy2child_gd1.count((*it).phy_index) > 0 && phy2child_gd2.count((*it).phy_index) > 0) {
            type = 5;
        } else if (phy2child_gd1.count((*it).phy_index) > 0) {
            if (gds[a].clade2.count((*it).phy_index) > 0) {
                type = 4;
            } else {
                type = 3;
            }
        } else if (phy2child_gd2.count((*it).phy_index) > 0) {
            if (gds[a].clade1.count((*it).phy_index) > 0) {
                type = 4;
            } else {
                type = 3;
            }
        } else if (gds[a].clade1.count((*it).phy_index) > 0 && gds[a].clade2.count((*it).phy_index) > 0) {
            type = 2;
        } else if (gds[a].clade1.count((*it).phy_index) > 0 || gds[a].clade2.count((*it).phy_index) > 0) {
            type = 1;
        }

        os << gds[a].gene_tree_id;
        os << "\t" << (gds[a].gd_id + 1);

        if (phy2child_gd1.count((*it).phy_index) > 0) os << "\t" << (phy2child_gd1[(*it).phy_index] + 1);
        else os << "\t" << "_";

        if (phy2child_gd2.count((*it).phy_index) > 0) os << "\t" << (phy2child_gd2[(*it).phy_index] + 1);
        else os << "\t" << "_";

        os << "\t" << (*phy_index2node[gds[a].phy_index]).name;
        os << "\t" << (*phy_index2node[(*it).phy_index]).name;
        os << "\t" << type;
        os << endl;

        for(tree<PhyNode>::pre_order_iterator b=it.begin();b!=it.end();b++) {
            long type=0;
            if(phy2child_gd1.count((*b).phy_index)>0 && phy2child_gd2.count((*b).phy_index)>0) {
                type=5;
            } else if(phy2child_gd1.count((*b).phy_index)>0) {
                if(gds[a].clade2.count((*b).phy_index)>0) {
                    type=4;
                } else {
                    type=3;
                }
            } else if(phy2child_gd2.count((*b).phy_index)>0) {
                if(gds[a].clade1.count((*b).phy_index)>0) {
                    type=4;
                } else {
                    type=3;
                }
            } else if(gds[a].clade1.count((*b).phy_index)>0 && gds[a].clade2.count((*b).phy_index)>0) {
                type=2;
            } else if(gds[a].clade1.count((*b).phy_index)>0 || gds[a].clade2.count((*b).phy_index)>0) {
                type=1;
            }

            os << gds[a].gene_tree_id;
            os << "\t" << (gds[a].gd_id+1);

            if(phy2child_gd1.count((*b).phy_index) > 0) os << "\t" << (phy2child_gd1[(*b).phy_index]+1);
            else os << "\t" <<"_";

            if(phy2child_gd2.count((*b).phy_index) > 0) os << "\t" << (phy2child_gd2[(*b).phy_index]+1);
            else os << "\t" <<"_";

            os << "\t" << (*phy_index2node[gds[a].phy_index]).name;
            os << "\t" << (*phy_index2node[(*b).phy_index]).name;
            os << "\t" << type;
            os << endl;
        }
    }
    os.close();
}

void Tree2GD::writeMedianKs4GDs(string out_name) {
    cerr<<"-> "<<out_name<<endl;
    ofstream os;
    os.open(out_name.c_str(), ios::out);
    if (os.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", out_name.c_str());
        return;
    }
    os<<"#cluster_id\tgd_id\tlevel\tspecies\tks\tnested\tdepth_var\tlen1\tlen2\tcomment"<<endl;
    for (long a = 0; a < gds.size(); a++) {
        if(!gds[a].save) continue;

        long nested=0;    //0 for single gd, 1 for higher gd
        for(long b=0;b<gds[a].child_gd1.size();b++) {
            long index=gds[a].child_gd1[b];
            if(gds[a].phy_index==gds[index].phy_index) {
                nested=1;
                break;
            }
        }
        for(long b=0;b<gds[a].child_gd2.size();b++) {
            long index=gds[a].child_gd2[b];
            if(gds[a].phy_index==gds[index].phy_index) {
                nested=1;
                break;
            }
        }

        os << gds[a].gene_tree_id;
        os << "\t" << (gds[a].gd_id+1);
        os << "\t" << (*phy_index2node[gds[a].phy_index]).name;
        os << "\t" << "average";
        if(gds[a].ks < 0) os << "\t" << "NA";
        else os << "\t" << gds[a].ks;
        os << "\t" << nested;
        os << "\t" << gds[a].depth_var;
        os << "\t" << gds[a].median_clade_len1;
        os << "\t" << gds[a].median_clade_len2;
        os << "\t" << gds[a].comment;
        os << endl;

        for(map<string,double>::iterator it=gds[a].species_ks.begin();it!=gds[a].species_ks.end();it++) {
            os << gds[a].gene_tree_id;
            os << "\t" << (gds[a].gd_id+1);
            os << "\t" << (*phy_index2node[gds[a].phy_index]).name;

            os << "\t" << it->first;
            if(it->second < 0) os << "\t" << "NA";
            else os << "\t" << it->second;
            os << "\t" << nested;
            os << "\t" << "_";
            os << "\t" << "_";
            os << "\t" << "_";
            os << "\t" << "_";
            os << endl;
        }
    }
    os.close();
}

void Tree2GD::writeOmega4EachSpecies(string out_folder) {
    cerr<<"-> "<<"ka/ks/omega for duplicated genes in each species"<<endl;

    //write kaks for each node
    ofstream os;
    string filename = out_folder + "/kaks.average";
    os.open(filename.c_str(), ios::out);
    if (os.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", filename.c_str());
        return;
    }
    os << "level\tka\tks\tomega" << endl;

    //write kaks for each species
    ofstream * oss = new ofstream[phy_leaves.size()];
    map<string, long> id2os_index;
    for(long i=0;i<phy_leaves.size();i++) {
        string filename = out_folder + "/kaks." + (*phy_leaves[i]).name;
        oss[i].open(filename.c_str(), ios::out);
        if (oss[i].fail()) {
            fprintf(stderr, "Can NOT open file for output: %s\n", filename.c_str());
            return;
        }
        oss[i] << "level\tgene1\tgene2\tka\tks\tomega" << endl;
        id2os_index[(*phy_leaves[i]).name]=i;
    }

    for (long a = 0; a < gds.size(); a++) {
        long num=0;
        double ave_ka=0;
        double ave_ks=0;
        double ave_omega=0;
        for (long b = 0; b < gds[a].gene_pairs.size(); b++) {
            long index=id2os_index[gds[a].gene_pairs[b].species_id];

            string id1=gds[a].gene_pairs[b].gene1;
            string id2=gds[a].gene_pairs[b].gene2;
            if(id1>id2) {
                string s=id1;
                id1=id2;
                id2=s;
            }

            if(gene2omega.count(id1)==0 || gene2omega[id1].count(id2)==0) continue;

            oss[index] << (*phy_index2node[gds[a].phy_index]).name;
            oss[index] << "\t" << id1;
            oss[index] << "\t" << id2;

            oss[index] << "\t" << gene2omega[id1][id2].ka;
            oss[index] << "\t" << gene2omega[id1][id2].ks;
            oss[index] << "\t" << gene2omega[id1][id2].omega<<endl;

            ave_ka+=gene2omega[id1][id2].ka;
            ave_ks+=gene2omega[id1][id2].ks;
            ave_omega+=gene2omega[id1][id2].omega;
            num++;
        }
        if(num>0) {
            ave_ka/=num;
            ave_ks/=num;
            ave_omega/=num;
            os << (*phy_index2node[gds[a].phy_index]).name;
            os << "\t" << ave_ka;
            os << "\t" << ave_ks;
            os << "\t" << ave_omega<<endl;
        }
    }

    for(long i=0;i<phy_leaves.size();i++) {
        oss[i].close();
    }
    delete[] oss;

    os.close();
}

void Tree2GD::writeRootedTrees(string out_folder) {
    cerr<<"-> "<<"rooted trees"<<endl;
    out_folder+="/rooted_trees";
    if (access(out_folder.c_str(), 0) == -1) mkdir(out_folder.c_str(), 0777);
    //output trees
    for(long i=0;i<g_trees.size();i++) {
        if(!g_trees[i].save) continue;
        //output rooted tree with gene names
        ofstream os;
        string filename=g_trees[i].tree_file;
//        if(!g_trees[i].is_true_tree) cout<<g_trees[i].tree_id<<"\t"<<filename<<endl;

        long site=filename.find_last_of('/');
        if(site>=0) filename=filename.substr(site+1,filename.length()-site);
        filename=out_folder+"/"+filename;

        os.open(filename.c_str(), ios::out);
        if (os.fail()) {
            fprintf(stderr, "Can NOT open file for output: %s for cluster %s\n", filename.c_str(),g_trees[i].tree_id.c_str());
            return;
        }

//        cerr<<filename<<endl;
//        printTree(stderr,g_trees[i].gene_tree,0);
        writeNewickTree(os, g_trees[i].gene_tree, g_trees[i].gene_tree.begin(),0);
        os.close();
    }
}

void Tree2GD::writeNewickTree(ofstream & os, tree<PhyNode> & curr_tree, tree<PhyNode>::iterator curr_it, long opt) {
    if(curr_it.number_of_children()==0) {
        if(opt==0) os<<(*curr_it).name<<":"<<(*curr_it).dist;
        else if(opt==1) os<<gene_idmap[(*curr_it).name]<<":"<<(*curr_it).dist;
        else if(opt==2) os<<(*curr_it).name;
    } else {
        os<<"(";
        tree<PhyNode>::sibling_iterator it=curr_it.begin();
        while(it!=curr_it.end()) {
            if(it!=curr_it.begin()) os<<",";
            writeNewickTree(os, curr_tree, it,opt);
            it++;
        }
        if(curr_it==curr_tree.begin()) os<<")"<<(*curr_it).name<<";"<<endl;
        else {
            if(opt==0 || opt==1) os<<")"<<(*curr_it).bootstrap<<":"<<(*curr_it).dist;
            else if(opt==2) os<<")"<<(*curr_it).name;//cdy_add
        }
    }
}

void Tree2GD::writeLowCopyOrthologs(string out_name1, string out_name2) {
    cerr<<"-> "<<out_name1<<endl;
    cerr<<"   "<<out_name2<<endl;

    map<long, long> phy2count;

    FILE * fp1 = fopen(out_name1.c_str(),"w");
    FILE * fp2 = fopen(out_name2.c_str(),"w");
    fprintf(fp1,"#species_tree\n");
    for (long a = 0; a < g_trees.size(); a++) {
        if(!g_trees[a].save) continue;
        fprintf(fp1,"#gene_tree: %s\t%s\n",g_trees[a].tree_id.c_str(),g_trees[a].tree_file.c_str());
        printTree(fp1,g_trees[a].gene_tree,0);

        for(tree<PhyNode>::leaf_iterator it=phy_tree.begin_leaf();it!=phy_tree.end_leaf();it++) phy2count[(*it).phy_index]=0;

        set<long> visited;
        for(tree<PhyNode>::pre_order_iterator b=g_trees[a].gene_tree.begin();b!=g_trees[a].gene_tree.end();b++) {
            if(visited.count((*b).index)) continue;
            if(phy2count.count((*b).phy_index)==0) continue;

            phy2count[(*b).phy_index]++;
            for(tree<PhyNode>::pre_order_iterator c=b.begin();c!=b.end();c++) {
                visited.insert((*c).index);
            }
        }

        bool is_low_copy=true;
        for(map<long,long>::iterator b=phy2count.begin();b!=phy2count.end();b++) {
            if(b->second!=1) {
                fprintf(fp1,"%s:\t%ld\n",(*phy_index2node[b->first]).name.c_str(),b->second);
                is_low_copy=false;
//                break;
            }
        }

        if(is_low_copy) {
            fprintf(fp1,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n");
            fprintf(fp2,"#%s\t%ld\n",g_trees[a].tree_id.c_str(),g_trees[a].gene_ids.size());
            for(int b=0;b<g_trees[a].gene_ids.size();b++) {
                string g_id=g_trees[a].gene_ids[b];
                string s_id=gene_idmap[g_id];
                fprintf(fp2,"%s\t%s\t%s\n",g_trees[a].tree_id.c_str(),s_id.c_str(),g_id.c_str());
            }
        }
    }
    fclose(fp1);
    fclose(fp2);
}

void Tree2GD::writePAML(string out_folder) {
    cerr<<"-> "<<"paml files"<<endl;
    string PAML="paml";
    string GENE_LIST="gene.list";
    string GENE_FAA="gene.faa";
    string GENE_CDS="gene.cds";
    string GENE_MUSCLE="gene.muscle";

    if (access((out_folder+"/"+PAML).c_str(), 0) == -1) mkdir((out_folder+"/"+PAML).c_str(), 0777);

    //write task1: selected faa/cds from the whole db according to the merged list
    string filename1=out_folder+"/run_paml_task1.sh";
    ofstream os1;
    os1.open(filename1.c_str(), ios::out);
    if (os1.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", filename1.c_str());
        return;
    }

    os1<<"rm selected.list selected.faa selected.cds"<<endl;

    //write task2: prepare files for PAML
    string filename2=out_folder+"/run_paml_task2.sh";
    ofstream os2;
    os2.open(filename2.c_str(), ios::out);
    if (os2.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", filename2.c_str());
        return;
    }

    //write task3: run PAML
    string filename3=out_folder+"/run_paml_task3.sh";
    ofstream os3;
    os3.open(filename3.c_str(), ios::out);
    if (os3.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", filename3.c_str());
        return;
    }

    for(long i=0;i<g_trees.size();i++) {
        if(!g_trees[i].save) continue;

        string sub_folder=PAML+"/C"+g_trees[i].tree_id;
        if (access((out_folder+"/"+sub_folder).c_str(), 0) == -1) mkdir((out_folder+"/"+sub_folder).c_str(), 0777);

        //write gene list
        string filename=out_folder+"/"+sub_folder+"/"+GENE_LIST;
        ofstream os;
        os.open(filename.c_str(), ios::out);
        if (os.fail()) {
            fprintf(stderr, "Can NOT open file for output: %s for cluster %s\n", filename.c_str(),g_trees[i].tree_id.c_str());
            return;
        }

        long num_leaves=0;
        for(tree<PhyNode>::leaf_iterator a=g_trees[i].gene_tree.begin_leaf();a!=g_trees[i].gene_tree.end_leaf();a++) {
            os<<(*a).name<<endl;
            num_leaves++;
        }
        os.close();

        //write gene tree
        filename=out_folder+"/"+sub_folder+"/in_tree";
        os.open(filename.c_str(), ios::out);
        if (os.fail()) {
            fprintf(stderr, "Can NOT open file for output: %s for cluster %s\n", filename.c_str(),g_trees[i].tree_id.c_str());
            return;
        }

        os<<num_leaves<<"\t1"<<endl;
        writeNewickTree(os, g_trees[i].gene_tree, g_trees[i].gene_tree.begin(),2);
        os.close();

        //write outgroup
        filename=out_folder+"/"+sub_folder+"/outgroup.list";
        os.open(filename.c_str(), ios::out);
        if (os.fail()) {
            fprintf(stderr, "Can NOT open file for output: %s for cluster %s\n", filename.c_str(),g_trees[i].tree_id.c_str());
            return;
        }

        for(long j=0;j<g_trees[i].og_ids.size();j++) os<<g_trees[i].og_ids[j]<<endl;
        os.close();

        os1<<"cat "<<sub_folder<<"/"<<GENE_LIST<<" >> selected.list"<<endl;

        os2<<"cp -r ../soft/* "<<sub_folder<<"/"<<endl;
        os2<<"java -jar ~/Java/MySelection12.jar -i selected.faa -l "<<sub_folder<<"/"<<GENE_LIST<<" -o "<<sub_folder<<"/"<<GENE_FAA<<endl;
        os2<<"java -jar ~/Java/MySelection12.jar -i selected.cds -l "<<sub_folder<<"/"<<GENE_LIST<<" -o "<<sub_folder<<"/"<<GENE_CDS<<endl;
        os2<<"muscle -in "<<sub_folder<<"/"<<GENE_FAA<<" -out "<<sub_folder<<"/"<<GENE_MUSCLE<<endl;
        os2<<"pal2nal.pl "<<sub_folder<<"/"<<GENE_MUSCLE<<" "<<sub_folder<<"/"<<GENE_CDS<<" -output paml > "<<sub_folder<<"/in_sequence"<<endl;

        os3<<"cd "<<sub_folder<<"/"<<endl;
        os3<<"codeml"<<endl;
    }

    os1<<"java -jar ~/Java/MySelection12.jar -i ../all.faa -l selected.list -o selected.faa"<<endl;
    os1<<"java -jar ~/Java/MySelection12.jar -i ../all.cds -l selected.list -o selected.cds"<<endl;

    os1.close();
    os2.close();
    os3.close();
}

void Tree2GD::writeClusteredAncestors(string out_name) {
    cerr<<"-> "<<out_name<<endl;
    ofstream os;
    os.open(out_name.c_str(), ios::out);
    if (os.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", out_name.c_str());
        return;
    }

    os<<"#cluster_id\tancestor\tcovered"<<endl;
    for (long a = 0; a < g_trees.size(); a++) {
        if(!g_trees[a].save) continue;
        os << g_trees[a].tree_id;
        os << "\t" << (*phy_index2node[g_trees[a].top_phy_index]).name;
        set<string> set1;
        for (tree<PhyNode>::leaf_iterator b = g_trees[a].gene_tree.begin_leaf(); b != g_trees[a].gene_tree.end_leaf(); b++) {
            if (gene_idmap.count((*b).name) > 0) set1.insert(gene_idmap[(*b).name]);
            else set1.insert("UNKNOWN");
        }
        os << "\t";
        for(set<string>::iterator b=set1.begin();b!=set1.end();b++) {
            if(b!=set1.begin()) os<<"-";
            os<<(*b);
        }
        os<<endl;
    }
    os.close();
}

void Tree2GD::writeIsoformCandidates(string out_folder) {
    cerr<<"-> "<<"isoform_candidates"<<endl;

    out_folder+="/isoform_candidates";
    string list_folder=out_folder+"/list";
    string faa_folder=out_folder+"/faa";
    string muscle_folder=out_folder+"/muscle";
    string isosvm_folder=out_folder+"/isosvm";

    if (access(out_folder.c_str(), 0) == -1) mkdir(out_folder.c_str(), 0777);
    if (access(list_folder.c_str(), 0) == -1) mkdir(list_folder.c_str(), 0777);
    if (access(faa_folder.c_str(), 0) == -1) mkdir(faa_folder.c_str(), 0777);
    if (access(muscle_folder.c_str(), 0) == -1) mkdir(muscle_folder.c_str(), 0777);
    if (access(isosvm_folder.c_str(), 0) == -1) mkdir(isosvm_folder.c_str(), 0777);

    string filename=out_folder+"/batch_isoforms.1";
    ofstream os;
    os.open(filename.c_str(), ios::out);
    if (os.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", filename.c_str());
        return;
    }

    //output isoforms
    set<long> species_phy_indecies;
    for(tree<PhyNode>::leaf_iterator i=phy_tree.begin_leaf();i!=phy_tree.end_leaf();i++) {
        if(genome_set.count((*i).name)>0) continue;
        species_phy_indecies.insert((*i).phy_index);
    }

    for(long i=0;i<g_trees.size();i++) {
        //output rooted tree with gene names
        if(!g_trees[i].save) continue;
//        printTree(stdout,g_trees[i].gene_tree,0);
        for (tree<PhyNode>::post_order_iterator it = g_trees[i].gene_tree.begin_post();it != g_trees[i].gene_tree.end_post();it++) {
            if(it==g_trees[i].gene_tree.begin() || it.number_of_children()==0) continue;
            tree<PhyNode>::iterator parent=g_trees[i].gene_tree.parent(it);
            if(species_phy_indecies.count((*parent).phy_index)==0 && species_phy_indecies.count((*it).phy_index)>0) {
                stringstream ss1;
                ss1 << "G_" << g_trees[i].tree_id;

                stringstream ss2;
                ss2 << "G_" << g_trees[i].tree_id<<"_"<<(*it).name;

                string list_name=list_folder+"/"+ss2.str()+".list";
                string in_faa_name="INFOLDER/"+ss1.str()+".faa";
                string out_faa_name=faa_folder+"/"+ss2.str()+".faa";
                string muscle_name=muscle_folder+"/"+ss2.str()+".faa.fst";
                string isosvm_name=isosvm_folder+"/"+ss2.str()+".isosvm";

                os<<"java -jar ~/Java/MySelection12.jar -l "<<list_name<<" -i "<<in_faa_name<<" -o "<<out_faa_name<<endl;
                os<<"muscle -in "<<out_faa_name<<" -out "<<muscle_name<<" -quiet"<<endl;
                os<<"isosvm.pl -fasta "<<muscle_name<<" > "<<isosvm_name<<endl;

                ofstream os1;
                os1.open(list_name.c_str(), ios::out);
                if (os1.fail()) {
                    fprintf(stderr, "Can NOT open file for output: %s for cluster %s\n", list_name.c_str(), g_trees[i].tree_id.c_str());
                    return;
                }

//                cout<<"***"<<(*it).name<<" "<<list_name<<endl;
                for(tree<PhyNode>::leaf_iterator leaf_it=g_trees[i].gene_tree.begin_leaf(it);leaf_it!=g_trees[i].gene_tree.end_leaf(it);leaf_it++) {
                    os1<<(*leaf_it).name<<endl;
//                    cout<<"\t"<<(*leaf_it).name<<endl;
                }
                os1.close();
            }
        }
    }

    os.close();
}

void Tree2GD::writeSisterClades(string out_name) {
    cerr<<"-> "<<out_name<<endl;
    ofstream os;
    os.open(out_name.c_str(), ios::out);
    if (os.fail()) {
        fprintf(stderr, "Can NOT open file for output: %s\n", out_name.c_str());
        return;
    }

    os<<"#cluster_id\tbootstrap\tsister1\tlevel1\tsister2\tlevel2"<<endl;
    for (long a = 0; a < g_trees.size(); a++) {
        if(!g_trees[a].save) continue;
        for (tree<PhyNode>::pre_order_iterator b = g_trees[a].gene_tree.begin(); b != g_trees[a].gene_tree.end(); b++) {
            if(b.number_of_children()!=2) continue;
            os << g_trees[a].tree_id<<"\t"<<(*b).bootstrap;
            for (tree<PhyNode>::sibling_iterator c = b.begin(); c != b.end(); c++) {
                os<<"\t"<<(*c).name<<"\t"<<(*phy_index2node[(*c).phy_index]).name;
            }
            os<<endl;
        }
    }
    os.close();
}

void Tree2GD::printTree(FILE* fp, tree<PhyNode>& sub_tree, long opt) {
    fprintf(fp, "============================================================\n");
    map<long, long> branch_points;
    tree<PhyNode>::pre_order_iterator it = sub_tree.begin();
    while (it != sub_tree.end()) {
        long depth = sub_tree.depth(it);
        if (it.number_of_children() > 1) branch_points[depth + 1] = it.number_of_children();

        string s = "";
        for (long a = 0; a < 3 * depth; a++) s += " ";
        for (long b = 0; b < depth; b++) {
            if (branch_points.count(b) > 0 && branch_points[b] > 0) {
                s[3 * b] = '|';
            }
        }
        if (branch_points.count(depth) > 0) branch_points[depth] = branch_points[depth] - 1;
//        if (taxa_id2leaf.count((*it).taxa_id) > 0 && skip_nodes[taxa_id2leaf[(*it).taxa_id]]) s[0] = '#';
//        string name=(*it).name;
//        if(name=="NA") name=(*it).name;
        if (opt == 0) {
            fprintf(fp, "%s%s (index=%ld, phy=%ld)\n", s.c_str(), (*it).name.c_str(), (*it).index, (*it).phy_index);
        } else if (opt == 1) {
            fprintf(fp, "%s%s %ld (gd=%ld N0=%ld tree=%ld)\n", s.c_str(), (*it).name.c_str(), (*it).index, (*it).gd_count, (*it).lineage_count, (*it).tree_count);
        } else if (opt == 2) {
            fprintf(fp, "%s%s (phy=%s, dist=%lf, bp=%lf)\n", s.c_str(), (*it).name.c_str(), (*phy_index2node[(*it).phy_index]).name.c_str(), (*it).dist, (*it).bootstrap);
        }
        //        cout<<s.c_str()<<(*it).taxa_id<<"  ("<<(*it).name<<")"<<endl;
        it++;
    }
}

/*
 *
 */
int main(int argc, char** argv) {
    if (argc < 5) usage(stderr, 0, argv[0]);

    string tree_file = argv[1];
    string idmap_file = argv[2];
    string list_file = argv[3];
    string out_prefix = argv[4];

    if(argc>5) {
        for(long i=5;i<argc;i++) {
            string opt=argv[i];
            if(startWith(opt, OPT_SPECIES)) {
                opt = opt.substr(OPT_SPECIES.length(),opt.length()-OPT_SPECIES.length());
                sscanf(opt.c_str(), "%ld", &MIN_SPECIES);

                if(MIN_SPECIES<0) {
                    fprintf(stderr, "wrong value for option %s: %s\n",OPT_SPECIES.c_str(),opt.c_str());
                    exit(0);
                }
            } else if(startWith(opt, OPT_BP)) {
                opt = opt.substr(OPT_BP.length(),opt.length()-OPT_BP.length());
                sscanf(opt.c_str(), "%ld", &MIN_BOOTSTRAP);

                if(MIN_BOOTSTRAP<0) {
                    fprintf(stderr, "wrong value for option %s: %s\n",OPT_BP.c_str(),opt.c_str());
                    exit(0);
                }
            }
            else if(startWith(opt, OPT_SPLIT)) {
                opt = opt.substr(OPT_SPLIT.length(),opt.length()-OPT_SPLIT.length());
                if(opt=="true") SPLIT_TREE=true;
                else if(opt=="false") SPLIT_TREE=false;
                else {
                    fprintf(stderr, "wrong value for option %s: %s\n",OPT_SPLIT.c_str(),opt.c_str());
                    exit(0);
                }
            }
            else if(startWith(opt, OPT_PRINT)) {
                opt = opt.substr(OPT_PRINT.length(),opt.length()-OPT_PRINT.length());
                if(opt=="true") PRINT=true;
                else if(opt=="false") PRINT=false;
                else {
                    fprintf(stderr, "wrong value for option %s: %s\n",OPT_PRINT.c_str(),opt.c_str());
                    exit(0);
                }
            }
            else if(startWith(opt, OPT_QUICK)) {
                opt = opt.substr(OPT_QUICK.length(),opt.length()-OPT_QUICK.length());
                QUICK_FILE = opt;
            }
            else if(startWith(opt, OPT_PARSER)) {
                opt = opt.substr(OPT_PARSER.length(),opt.length()-OPT_PARSER.length());
                PARSER_FILE = opt;
            }
            else if(startWith(opt, OPT_PAML)) {
                opt = opt.substr(OPT_PAML.length(),opt.length()-OPT_PAML.length());
                if(opt=="true") SAVE_PAML=true;
                else if(opt=="false") SAVE_PAML=false;
                else {
                    fprintf(stderr, "wrong value for option %s: %s\n",OPT_PAML.c_str(),opt.c_str());
                    exit(0);
                }
            }
            else if(startWith(opt, OPT_OMEGA)) {
                opt = opt.substr(OPT_OMEGA.length(),opt.length()-OPT_OMEGA.length());
                OMEGA_FILE = opt;
            }
            else if(startWith(opt, OPT_SUBBP)) {
                opt = opt.substr(OPT_SUBBP.length(),opt.length()-OPT_SUBBP.length());
                sscanf(opt.c_str(), "%ld", &MIN_SUB_CLADE_BP);

                if(MIN_SUB_CLADE_BP<0) {
                    fprintf(stderr, "wrong value for option %s: %s\n",OPT_SUBBP.c_str(),opt.c_str());
                    exit(0);
                }
            }
            else if(startWith(opt, OPT_GENOME)) {
                opt = opt.substr(OPT_GENOME.length(),opt.length()-OPT_GENOME.length());
                GENOME_FILE = opt;
            }
            else if(startWith(opt, OPT_ISOFORM)) {
                opt = opt.substr(OPT_ISOFORM.length(),opt.length()-OPT_ISOFORM.length());
                ISOFORM_FILE = opt;
            }
            else if(startWith(opt, OPT_SAVETREE)) {
                opt = opt.substr(OPT_SAVETREE.length(),opt.length()-OPT_SAVETREE.length());
                if(opt=="true") SAVE_ROOTED=true;
                else if(opt=="false") SAVE_ROOTED=false;
                else {
                    fprintf(stderr, "wrong value for option %s: %s\n",OPT_SAVETREE.c_str(),opt.c_str());
                    exit(0);
                }
            }
            else if(startWith(opt, OPT_DEEPVAR)) {
                opt = opt.substr(OPT_DEEPVAR.length(),opt.length()-OPT_DEEPVAR.length());
                sscanf(opt.c_str(), "%ld", &MAX_DEEP_VAR);

                if(MAX_DEEP_VAR<0) {
                    fprintf(stderr, "wrong value for option %s: %s\n",OPT_DEEPVAR.c_str(),opt.c_str());
                    exit(0);
                }
            }
            else if(startWith(opt, OPT_ROOT)) {
                opt = opt.substr(OPT_ROOT.length(),opt.length()-OPT_ROOT.length());
                if(opt!=KW_MIN_TOPO_ERR && opt!=KW_MAX_DUP_SCORE && opt!=KW_MAX_DUP_BRANCH)
                {
                    fprintf(stderr, "wrong value for option %s: %s\n",OPT_ROOT.c_str(),opt.c_str());
                    exit(0);
                }
                ROOT_METHOD=opt;
            }
            else usage(stderr, 0, argv[0]);
        }
    }

    fprintf(stderr, "%s: %ld\n",OPT_SPECIES.c_str(),MIN_SPECIES);
    fprintf(stderr, "%s: %ld\n",OPT_BP.c_str(),MIN_BOOTSTRAP);
    fprintf(stderr, "%s: %ld\n",OPT_SUBBP.c_str(),MIN_SUB_CLADE_BP);
    fprintf(stderr, "%s: %s\n",OPT_SPLIT.c_str(),SPLIT_TREE ? "true" : "false");
    fprintf(stderr, "%s: %s\n",OPT_QUICK.c_str(),QUICK_FILE.c_str());
    fprintf(stderr, "%s: %s\n",OPT_PARSER.c_str(),PARSER_FILE.c_str());
    fprintf(stderr, "%s: %s\n",OPT_PAML.c_str(),SAVE_PAML ? "true" : "false");
    fprintf(stderr, "%s: %s\n",OPT_OMEGA.c_str(),OMEGA_FILE.c_str());
    fprintf(stderr, "%s: %s\n",OPT_GENOME.c_str(),GENOME_FILE.c_str());
    fprintf(stderr, "%s: %s\n",OPT_ISOFORM.c_str(),ISOFORM_FILE.c_str());
    fprintf(stderr, "%s: %s\n",OPT_SAVETREE.c_str(),SAVE_ROOTED ? "true" : "false");
    fprintf(stderr, "%s: %ld\n",OPT_DEEPVAR.c_str(),MAX_DEEP_VAR);
    fprintf(stderr, "%s: %s\n",OPT_ROOT.c_str(),ROOT_METHOD.c_str());

    Tree2GD tree2gd(tree_file,idmap_file,list_file,out_prefix);
    tree2gd.execute();
    return 0;
}
