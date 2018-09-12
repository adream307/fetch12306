#include<iostream>
#include<fstream>
#include<string>

using namespace std;

int main(int argc,const char* argv[])
{
	ifstream infile(argv[1]);
	if(infile.bad()) return -1;
	string s;
	while(getline(infile,s))
	{
		if(s=="") continue;
		cout << s << endl;
	}
	return 0;
}
