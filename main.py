from lexicalAnalyzer import generateOuput, classifyToken, breakWords
from syntaxAnalyzer import syntaxAnalyzer
from semanticAnalyzer import semanticAnalyzer, report


with open("D:\\Uni Kaam\\3rd Year\\6th Semester\\CC\\MyProject\\io-files\\inputFile.txt", "r") as inputfile:
    input_text = inputfile.read()

# generatedTokens = breakWords(input_text)
# classifiedTokens = classifyToken(generatedTokens)
# output_text = generateOuput(classifiedTokens)

tokenList = classifyToken(breakWords(input_text))

synError, check = syntaxAnalyzer(tokenList)
if (check):
    print("\nSyntax Result :")
    print("\t***  INPUT COMPLETELY PARSED WITH COMPLETE TREE  ***\n")
    x = semanticAnalyzer(tokenList)
    print("\nSemantic Result :")
    print("\t***  ", str(x).upper(), "  ***\n")

    with open("D:\\Uni Kaam\\3rd Year\\6th Semester\\CC\\MyProject\\io-files\\outputFile.txt", "w") as outputfile:
        outputfile.write(report())

else:
    print("\n\t***  SYNTAX ERROR  ***\n")
    print("ERROR:",synError)

    with open("D:\\Uni Kaam\\3rd Year\\6th Semester\\CC\\MyProject\\io-files\\outputFile.txt", "w") as outputfile:
        outputfile.write(synError)
        outputfile.write(generateOuput(tokenList))
