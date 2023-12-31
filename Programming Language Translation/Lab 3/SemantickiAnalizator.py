import ulaz
import copy
from Stablo import *

korijen = ulaz.ulaz()

allDeclared = True 
whitespaces = 0

def jebroj(broj):
    if not broj.isdigit():
        return False
    broj = int(broj)
    return (-2147483648 <= broj and broj <= 2147483647)

def je1do1024(broj):
    if not broj.isdigit():
        return False
    broj = int(broj)
    return (0 < broj and broj <= 1024)


# Ova funkcija je dosta sussy, idem ja ponovno napisat
# def jeznak(znak):
#     if znak[0] != '\"':
#         return False
#     if znak[len(znak) - 1] != "\"":
#         return False
#     znak = znak[1:(len(znak)-1)]
#     if(len(znak) == 1 and znak[0] != "\\"):
#         return True
#     elif(len(znak) == 2 and znak[0] == "\\" and znak[1] in ("t", "n", "0", "\'", "\"", "\\")):
#         return False
#     return False

def jeznak(znak):
    if znak[0] == '\"': return False
    znak = znak[1:len(znak) - 1]
    return len(znak) == 1 or (len(znak) == 2 and znak[0] == "\\" and znak[1] in ("t", "n", "0", "\'", "\"", "\\"))


def jenizznakova(niz):
    if niz[0] != '\"':
        return False
    if niz[len(niz) - 1] != "\"":
        return False

    it = 0
    while("\\" in niz[it:]):
        it = niz[it:].index("\\")
        if it + 1 == len(niz) or niz[it + 1] not in ("t", "n", "0", "\'", "\"", "\\"):
            return False
        it += 2
    return True

def jeNizX(str):
    return not isinstance(str, Funkcija) and str[0:4] == "niz(" and str[len(str)-1] == ")" and jeX(str[4:(len(str)-1)])

def jeNizT(str):
    return not isinstance(str, Funkcija) and str[0:4] == "niz(" and str[len(str)-1] == ")" and jeT(str[4:(len(str)-1)])

def jeNizConstX(str):
    return not isinstance(str, Funkcija) and str[0:4] == "niz(" and str[len(str)-1] == ")" and jeConstX(str[4:(len(str)-1)])

def jeNizConstT(str):
    return not isinstance(str, Funkcija) and str[0:4] == "niz(" and str[len(str)-1] == ")" and jeConstT(str[4:(len(str)-1)])

# Ovo je suvisno
def jeConstX(str):
    return not isinstance(str, Funkcija) and str[0:6] == "const(" and str[len(str)-1] == ")" and jeX(str[6:(len(str)-1)])
#---------------

def jeConstT(str):
    return not isinstance(str, Funkcija) and str[0:6] == "const(" and str[len(str)-1] == ")" and jeT(str[6:(len(str)-1)])

def jeX(str):
    #return str == "const(int)" or str == "const(char)" or str == "int" or str == "char" or str == "X"
    return jeT(str) or jeConstT(str)

def jeT(str):
    return str == "int" or str == "char" or str == "T"

def ImplicitnoXToY(x, y): # Gleda vrijedi li x ~ y, nisam sto posto ako je tranzitivno okruzenje potpuno, cini mi se da je, ali mi špurijus govori da nije
    #return x == y or jeT(x) and jeConstT(y) and x != "char" and y != int or jeConstT(x) and jeT(y) and x != "char" and y != int  or x == "char" and y == "int" or jeNizT(x) and jeNizConstT(y) and x != "char" and y != int
    #return (x == y or jeT(x) and jeConstT(y) or jeConstT(x) and jeT(y) or jeNizT(x) and jeNizConstT(y)) and x != "int" and y != "char" or x == "char" and y == "int"
    #return (x == y or jeT(x) and (jeConstT(y) or jeT(y)) or jeConstT(x) and (jeT(y) or jeConstT(y)) or jeNizT(x) and (jeNizConstT(y) or jeNizT(y))) and x != "int" and y != "char" or x == "char" and y == "int"
    return (jeT(x) and jeX(y) or jeConstT(x) and jeX(y) or jeNizT(x) and jeNizX(y)) and not (x == "int" and y == "char")

def EksplicitnoXToY(x, y):
    return jeX(x) and jeX(y)
    #return x == "char" and y == "int"
    #return ImplicitnoXToY(x, y) #? ovako radi ig

def checkFunkcije(tablica_IDN, djelokrug):
    global allDeclared
    for value in tablica_IDN.values():
        if isinstance(value.tip, Funkcija) and not value.tip.definirana and djelokrug[-1] == value.djelokrug:
            allDeclared = False
            break

def zavrsnaProvjera(tablica_IDN, djelokrug):
    checkFunkcije(tablica_IDN, djelokrug)
    if not ("main" in tablica_IDN.keys() and isinstance(tablica_IDN["main"].tip, Funkcija) and tablica_IDN["main"].tip.params == "void" and tablica_IDN["main"].tip.pov == "int"):
        print("main")
    elif not allDeclared:
        print("funkcija")
    else:
        print("Uspijeh")


def provjeri(cvor, tablica_IDN, djelokrug):
    # djeca = None
    # if isinstance(cvor, UnutarnjiCvor):
    #     djeca = cvor.djeca

    # global whitespaces
    # for i in range(whitespaces):
    #     print(" ", end ="")
    # whitespaces+=1
    # print(cvor.znak, "->", cvor.djeca)
    djeca = cvor.djeca

    if(cvor.znak == "<primarni_izraz>"):

        if(djeca[0].znak == "IDN"):
            #if tablica_IDN[djeca[0].vrijednost].tip == None:
            if not djeca[0].vrijednost in tablica_IDN.keys():
                print("<primarni_izraz> ::= " + str(djeca[0]))
                return False
            
            #TODO ovdje nesto ne valja vjv
            tip = tablica_IDN[djeca[0].vrijednost].tip
            #print(tip.params, tip.pov)

            # if isinstance(tablica_IDN[djeca[0].vrijednost].tip, Funkcija):
            #     tip = tablica_IDN[djeca[0].vrijednost].tip.params
            # else:
            #     tip = tablica_IDN[djeca[0].vrijednost].tip

            # tip će biti ili string "int", "char" i tako
            # ili tuple oblika (params, pov) ("void", "void"), (["int", "int"], "char") i tako

            cvor.tip = tip
            cvor.lizraz = not isinstance(tip, Funkcija) and jeT(tip) 
            


        elif(djeca[0].znak == "BROJ"):
            if not jebroj(djeca[0].vrijednost):
                print("<primarni_izraz> ::= " + str(djeca[0]))
                return False

            cvor.tip = "int"
            cvor.lizraz = False


        elif(djeca[0].znak == "ZNAK"):
            if not jeznak(djeca[0].vrijednost):
                print("<primarni_izraz> ::= " + str(djeca[0]))
                return False

            cvor.tip = "char"
            cvor.lizraz = False



        elif(djeca[0].znak == "NIZ_ZNAKOVA"):
            if not jenizznakova(djeca[0].vrijednost):
                print("<primarni_izraz> ::= " + str(djeca[0]))
                return False

            cvor.tip = "niz(const(char))"
            cvor.lizraz = False
            cvor.brelem = len(djeca[0].vrijednost) - 2
            
            
            
            #Nadopuniti sve izraze koji generiraju NIZ_ZNAKOVA sa brelem!!!!!!!!


        elif(djeca[0].znak == "L_ZAGRADA"):
            if not provjeri(djeca[1], tablica_IDN, djelokrug):
                return False

            cvor.tip = djeca[1].tip
            cvor.lizraz = djeca[1].lizraz

        
        else:
            print("POGREŠKA U <primarni_izraz>")
            return False


    elif(cvor.znak == "<postfiks_izraz>"):
        if(djeca[0].znak == "<primarni_izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem
        
        elif(djeca[1].znak == "OP_INC" or djeca[1].znak == "OP_DEC"):
            cvor.tip = "int"
            cvor.lizraz = False

            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

            if not djeca[0].lizraz or not jeX(djeca[0].tip): #Ponovno pretpostavka da je X jednako kao implicitno castabilan u int
                print("<postfiks_izraz> ::= <postfiks_izraz> " + str(djeca[1]))
                return False
        
        elif(djeca[2].znak == "<izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

            if not jeNizX(djeca[0].tip): #Nije implicitno kastabilan u int (nisam siguran je li to isto kao X, tj. je li char implicitno castabilan u int u ovom)
                print("<postfiks_izraz> ::= <postfiks_izraz> " + str(djeca[1]) + " <izraz> " + str(djeca[3]))
                return False

            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False

            if not jeX(djeca[2].tip):
                print("<postfiks_izraz> ::= <postfiks_izraz> " + str(djeca[1]) + " <izraz> " + str(djeca[3]))
                return False
                
            cvor.tip = djeca[0].tip[4:(len(djeca[0].tip)-1)]
            cvor.lizraz = not jeConstT(cvor.tip)


        elif(djeca[2].znak == "D_ZAGRADA"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

            if not (isinstance(djeca[0].tip, Funkcija) and djeca[0].tip.params == "void"):
                print("<postfiks_izraz> ::= <postfiks_izraz> " + str(djeca[1]) + " " + str(djeca[2]))
                return False

            cvor.tip = djeca[0].tip.pov
            cvor.lizraz = False


        elif(djeca[2].znak == "<lista_argumenata>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            #print(isinstance(djeca[0].tip, Funkcija), isinstance(djeca[0].tip.params, list), len(djeca[0].tip.params), len(djeca[2].tipovi))
            if not (isinstance(djeca[0].tip, Funkcija) and isinstance(djeca[0].tip.params, list) and len(djeca[0].tip.params) == len(djeca[2].tipovi)):
                print("<postfiks_izraz> ::= <postfiks_izraz> " + str(djeca[1]) + " <lista_argumenata> " + str(djeca[3]))
                return False

            for i in range(len(djeca[2].tipovi)):
                if not ImplicitnoXToY(djeca[2].tipovi[i], djeca[0].tip.params[i]):
                    #print(djeca[0].tip.params[i], djeca[2].tipovi[i])
                    print("<postfiks_izraz> ::= <postfiks_izraz> " + str(djeca[1]) + " <lista_argumenata> " + str(djeca[3]))
                    return False

            cvor.tip = djeca[0].tip.pov
            cvor.lizraz = False


      

        else:
            print("POGREŠKA U <postfiks_izraz>")
            return False

        
    elif(cvor.znak == "<lista_argumenata>"):
        if(djeca[0].znak == "<izraz_pridruzivanja>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

            cvor.tipovi = [ djeca[0].tip ]
            

        elif(djeca[0].znak == "<lista_argumenata>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            
            cvor.tipovi = djeca[0].tipovi + [ djeca[2].tip ] 

        
        else:
            print("POGREŠKA U <lista_argumenata>")
            return False
        


    elif(cvor.znak == "<unarni_izraz>"):
        if(djeca[0].znak == "<postfiks_izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem

        elif(djeca[1].znak == "<unarni_izraz>"):
            if not provjeri(djeca[1], tablica_IDN, djelokrug):
                return False
            
            if not (djeca[1].lizraz and jeX(djeca[1].tip)):
                print("<unarni_izraz> ::= " + str(djeca[0]) + " <unarni_izraz>")
                return False

            cvor.tip = "int"
            cvor.lizraz = False


        elif(djeca[0].znak == "<unarni_operator>"):
            if not provjeri(djeca[1], tablica_IDN, djelokrug):
                return False
            
            if not jeX(djeca[1].tip):
                print("<unarni_izraz> ::= <unarni_operator> <cast_izraz>")
                return False    

            cvor.tip = "int"
            cvor.lizraz = False

        else: 
            print("POGREŠKA U <unarni_izraz>")
            return False

    #<unarni_izraz> mozda

    elif(cvor.znak == "<cast_izraz>"):
        if(djeca[0].znak == "<unarni_izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem

        
        elif(djeca[0].znak == "L_ZAGRADA"):
            if not provjeri(djeca[1], tablica_IDN, djelokrug):
                return False
            if not provjeri(djeca[3], tablica_IDN, djelokrug):
                return False
            
            if not EksplicitnoXToY(djeca[3].tip, djeca[1].tip):
                print("<cast_izraz> ::= "+str(djeca[0])+" <ime_tipa> "+str(djeca[2])+" <cast_izraz>")
                return False

            cvor.tip = djeca[1].tip
            cvor.lizraz = False

        else: 
            print("POGREŠKA U <cast_izraz>")
            return False



    elif(cvor.znak == "<ime_tipa>"):
        if(djeca[0].znak == "<specifikator_tipa>"):            
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

            cvor.tip = djeca[0].tip

        
        elif(djeca[0].znak == "KR_CONST"):
            if not provjeri(djeca[1], tablica_IDN, djelokrug):
                return False

            if (djeca[0].tip == "void"):
                print("<ime_tipa> ::= " + str(djeca[0]) + " <specifikator_tipa>")
                return False
            
            cvor.tip = "const(" + djeca[1].tip + ")"

        else:
            print("POGREŠKA U <ime_tipa>")
            return False



    elif(cvor.znak == "<specifikator_tipa>"):
        if(djeca[0].znak == "KR_VOID"):
            cvor.tip = "void"
        
        elif(djeca[0].znak == "KR_CHAR"):
            cvor.tip = "char"
        
        elif(djeca[0].znak == "KR_INT"):
            cvor.tip = "int"

        else:
            print("POGREŠKA U <specifikator_tipa>")
            return False
        


    elif(cvor.znak == "<multiplikativni_izraz>"):
        if(djeca[0].znak == "<cast_izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

            # cvor.tip = "void"
            # cvor.lizraz = djeca[0].lizraz
            # cvor.brelem = djeca[0].brelem 
            # ??

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem


        
        elif(djeca[0].znak == "<multiplikativni_izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[0].tip):
                print("<multiplikativni_izraz> ::= <multiplikativni_izraz> " + str(djeca[1]) + " <cast_izraz>")
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[2].tip):
                print("<multiplikativni_izraz> ::= <multiplikativni_izraz> " + str(djeca[1]) + " <cast_izraz>")
                return False
            
            cvor.tip = "int"
            cvor.lizraz = False


        else:
            print("POGREŠKA U <multiplikativni_izraz>")
            return False
    


    elif(cvor.znak == "<aditivni_izraz>"):
        if(djeca[0].znak == "<multiplikativni_izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem
        
        elif(djeca[0].znak == "<aditivni_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = False

            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[0].tip):
                print("<aditivni_izraz> ::= <aditivni_izraz> " + str(djeca[1]) + " <multiplikativni_izraz>")
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[2].tip):
                print("<aditivni_izraz> ::= <aditivni_izraz> " + str(djeca[1]) + " <multiplikativni_izraz>")
                return False        
        else:
            print("POGREŠKA U <aditivni_izraz>")
            return False
        

    elif(cvor.znak == "<odnosni_izraz>"):
        if(djeca[0].znak == "<aditivni_izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem

        elif(djeca[0].znak == "<odnosni_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = False

            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[0].tip):
                print("<odnosni_izraz> ::= <odnosni_izraz> " + str(djeca[1]) + " <aditivni_izraz>")
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[2].tip):
                print("<odnosni_izraz> ::= <odnosni_izraz> " + str(djeca[1]) + " <aditivni_izraz>")
                return False
        
        else:
            print("POGREŠKA U <odnosni_izraz>")
            return False



    elif(cvor.znak == "<jednakosni_izraz>"):
        if(djeca[0].znak == "<odnosni_izraz>"):        
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem    
        
        elif(djeca[0].znak == "<jednakosni_izraz>"):   
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[0].tip):
                print("<jednakosni_izraz> ::= <jednakosni_izraz> " + str(djeca[1]) + " <odnosni_izraz>")
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[2].tip):
                print("<jednakosni_izraz> ::= <jednakosni_izraz> " + str(djeca[1]) + " <odnosni_izraz>")
                return False   

            cvor.tip = "int"
            cvor.lizraz = False

        else:
            print("POGREŠKA U <jednakosni_izraz>")
            return False
    

    
    elif(cvor.znak == "<bin_i_izraz>"):
        if(djeca[0].znak == "<jednakosni_izraz>"):       
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem
        
        elif(djeca[0].znak == "<bin_i_izraz>"):
            cvor.tip = "int"
            cvor.lizraz = False
        
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[0].tip):
                print("<bin_i_izraz> ::= <bin_i_izraz> " + str(djeca[1]) + " <jednakosni_izraz>")
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[2].tip):
                print("<bin_i_izraz> ::= <bin_i_izraz> " + str(djeca[1]) + " <jednakosni_izraz>")
                return False
        
        else:
            print("POGREŠKA U <bin_i_izraz>")
            return False

    
    elif(cvor.znak == "<bin_xili_izraz>"):
        if(djeca[0].znak == "<bin_i_izraz>"):       
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem

        elif(djeca[0].znak == "<bin_xili_izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[0].tip):
                print("<bin_xili_izraz> ::= <bin_xili_izraz> "+str(djeca[1])+ " <bin_i_izraz>")
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[2].tip):
                print("<bin_xili_izraz> ::= <bin_xili_izraz> "+str(djeca[1])+ " <bin_i_izraz>")
                return False
            cvor.tip = "int"
            cvor.lizraz = False

        
        else:
            print("POGREŠKA U <bin_xili_izraz>")
            return False
    
    elif(cvor.znak == "<bin_ili_izraz>"):
        if(djeca[0].znak == "<bin_xili_izraz>"):        
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem
        
        elif(djeca[0].znak == "<bin_ili_izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[0].tip):
                print("<bin_ili_izraz> ::= <bin_ili_izraz> "+str(djeca[1])+" <bin_xili_izraz>")
                return False

            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[2].tip):
                print("<bin_ili_izraz> ::= <bin_ili_izraz> "+str(djeca[1])+" <bin_xili_izraz>")
                return False        
            cvor.tip = "int"
            cvor.lizraz = False
        
        else:
            print("POGREŠKA U <bin_ili_izraz>")
            return False
    
    elif(cvor.znak == "<log_i_izraz>"):
        if(djeca[0].znak == "<bin_ili_izraz>"):       
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem

        elif(djeca[0].znak == "<log_i_izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[0].tip):
                print("<log_i_izraz> ::= <log_i_izraz> "+str(djeca[1])+" <bin_ili_izraz>")
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[2].tip):
                print("<log_i_izraz> ::= <log_i_izraz> "+str(djeca[1])+" <bin_ili_izraz>")
                return False

            cvor.tip = "int"
            cvor.lizraz = False

        else:
            print("POGREŠKA U <log_i_izraz>")
            return False
    

    elif(cvor.znak == "<log_ili_izraz>"):
        if(djeca[0].znak == "<log_i_izraz>"):       
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem
        
        elif(djeca[0].znak == "<log_ili_izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[0].tip):
                print("<log_ili_izraz> ::= <log_ili_izraz> "+str(djeca[1])+" <log_i_izraz>")
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[2].tip):
                print("<log_ili_izraz> ::= <log_ili_izraz> "+str(djeca[1])+" <log_i_izraz>")
                return False
            
            cvor.tip = "int"
            cvor.lizraz = False

        else:
            print("POGREŠKA U <log_ili_izraz>")
            return False

    elif(cvor.znak == "<izraz_pridruzivanja>"):
        if(djeca[0].znak == "<log_ili_izraz>"):        
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz
            cvor.brelem = djeca[0].brelem 

        elif(djeca[0].znak == "<postfiks_izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not djeca[0].lizraz:
                print("<izraz_pridruzivanja> ::= <postfiks_izraz> "+str(djeca[1])+" <izraz_pridruzivanja>")
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not ImplicitnoXToY(djeca[2].tip, djeca[0].tip):
                print("<izraz_pridruzivanja> ::= <postfiks_izraz> "+str(djeca[1])+" <izraz_pridruzivanja>")
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = False

        else:
            print("POGREŠKA U <izraz_pridruzivanja>")
            return False
    
    elif(cvor.znak == "<izraz>"):
        if(djeca[0].znak == "<izraz_pridruzivanja>"):        
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            
            cvor.tip = djeca[0].tip
            cvor.lizraz = djeca[0].lizraz

        
        elif(djeca[0].znak == "<izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False

            cvor.tip = djeca[0].tip
            cvor.lizraz = False

        else:
            print("POGREŠKA U <izraz>")
            return False
    
    #4.4.5 Naredbena struktura programa
    elif(cvor.znak == "<slozena_naredba>"):
        if(djeca[1].znak == "<lista_naredbi>"):
            if not provjeri(djeca[1], copy.deepcopy(tablica_IDN), djelokrug):
                return False
        
        elif(djeca[1].znak == "<lista_deklaracija>"):
            nova_tablica = copy.deepcopy(tablica_IDN)
            if not provjeri(djeca[1], nova_tablica, djelokrug):
                return False
            if not provjeri(djeca[2], nova_tablica, djelokrug):
                return False

        else:
            print("POGREŠKA U <slozena_naredba>")
            return False

    
    elif(cvor.znak == "<lista_naredbi>"):
        if(djeca[0].znak == "<naredba>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

        elif(djeca[0].znak == "<lista_naredbi>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not provjeri(djeca[1], tablica_IDN, djelokrug):
                return False

        else:
            print("POGREŠKA U <lista_naredbi>")
            return False

    elif(cvor.znak == "<naredba>"):
        #TODO mozda treba razdvojit
        if djeca[0].znak == "<slozena_naredba>" or djeca[0].znak == "<naredba_petlje>":

            if not provjeri(djeca[0], copy.deepcopy(tablica_IDN), djelokrug[:] + [djelokrugPodatak("BLOK", len(djelokrug) + 1)]):
                return False
        else:
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

    elif(cvor.znak == "<izraz_naredba>"):
        if(djeca[0].znak == "TOCKAZAREZ"):
            cvor.tip = "int"

        elif(djeca[0].znak == "<izraz>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

            cvor.tip = djeca[0].tip

        else:
            print("POGREŠKA U <izraz_naredba>")
            return False
    
    elif(cvor.znak == "<naredba_grananja>"):
        if(len(djeca) == 5):
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False

            if not jeX(djeca[2].tip):
                print("<naredba_grananja> ::= "+str(djeca[0])+" "+str(djeca[1])+" <izraz> "+str(djeca[3])+" <naredba>")
                return False

            if not provjeri(djeca[4], tablica_IDN, djelokrug):
                return False
        

        elif(len(djeca) == 7):
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False

            if not jeX(djeca[2].tip):
                print("<naredba_grananja> ::= " + str(djeca[0]) + " <izraz> "+str(djeca[2])+" <naredba> " +str(djeca[4])+ " <naredba>")
                return False

            if not provjeri(djeca[4], tablica_IDN, djelokrug):
                return False
            if not provjeri(djeca[6], tablica_IDN, djelokrug):
                return False
        
        else:
            print("POGREŠKA U <naredba_grananja>")
            return False
        
    elif(cvor.znak == "<naredba_petlje>"):
        if(djeca[0].znak == "KR_WHILE"):
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[2].tip):
                print("<naredba_petlje> ::= "+str(djeca[0])+" "+str(djeca[1])+" <izraz> "+str(djeca[3])+" <naredba>")
                return False
            if not provjeri(djeca[4], tablica_IDN, djelokrug[:] + [djelokrugPodatak("PETLJA", len(djelokrug) + 1)]):
                return False
        
        elif(djeca[4].znak == "D_ZAGRADA"):
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not provjeri(djeca[3], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[3].tip):
                print("<naredba_petlje> ::= "+str(djeca[0])+" "+str(djeca[1])+" <izraz_naredba> <izraz_naredba> "+str(djeca[4])+" <naredba>")
                return False
            if not provjeri(djeca[5], tablica_IDN, djelokrug[:] + [djelokrugPodatak("PETLJA", len(djelokrug) + 1)]):
                return False

        elif(djeca[4].znak == "<izraz>"):
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if not provjeri(djeca[3], tablica_IDN, djelokrug):
                return False
            if not jeX(djeca[3].tip):
                print("<naredba_petlje> ::= "+str(djeca[0])+" "+str(djeca[1])+" <izraz_naredba> <izraz_naredba> <izraz> "+str(djeca[5])+" <naredba>")
                return False
            if not provjeri(djeca[4], tablica_IDN, djelokrug):
                return False
            if not provjeri(djeca[6], tablica_IDN, djelokrug[:] + [djelokrugPodatak("PETLJA", len(djelokrug) + 1)]):
                return False

        else:
            print("POGREŠKA U <naredba_petlje>")
            return False
    
    elif(cvor.znak == "<naredba_skoka>"):
        if(djeca[0].znak == "KR_CONTINUE" or djeca[0].znak == "KR_BREAK"):
            # if not djelokrug[len(djelokrug)-1].vrsta == "PETLJA":
            #     print("<naredba_skoka> ::= "+ str(djeca[0]) + " " + str(djeca[1]))
            #     return False

            for env in djelokrug:
                if env.vrsta == "PETLJA":
                    break
            else:
                print("<naredba_skoka> ::= "+ str(djeca[0]) + " " + str(djeca[1]))
                return False

        elif(djeca[1].znak == "TOCKAZAREZ"):
            i = len(djelokrug) - 1
            while(djelokrug[i].vrsta != "GLOBAL"):
                if isinstance(djelokrug[i].vrsta, Funkcija):
                    funkcija = djelokrug[i].vrsta
                    if funkcija.pov != "void":
                        print("<naredba_skoka> ::= "+ str(djeca[0]) + " " + str(djeca[1]))
                        return False
                    else:
                        return True
                i -= 1
            print("<naredba_skoka> ::= "+ str(djeca[0]) + " " + str(djeca[1]))
            return False


        elif(djeca[1].znak == "<izraz>"):
            if not provjeri(djeca[1], tablica_IDN, djelokrug):
                return False
            i = len(djelokrug) - 1
            while(djelokrug[i].vrsta != "GLOBAL"):
                if isinstance(djelokrug[i].vrsta, Funkcija):
                    funkcija = djelokrug[i].vrsta
                    if not ImplicitnoXToY(djeca[i].tip, funkcija.pov):
                    #if not(ImplicitnoXToY(djeca[1].tip, funkcija.pov) or (isinstance(djeca[1].tip, Funkcija) and not ImplicitnoXToY(djeca[1].tip.pov, funkcija.pov))):
                        # print("here")
                        # print(djeca[i].tip, funkcija.pov)
                        print("<naredba_skoka> ::= "+ str(djeca[0]) + " <izraz> " + str(djeca[2]))
                        return False
                    else:
                        return True
                i -= 1
            print("<naredba_skoka> ::= "+ str(djeca[0]) + " <izraz> " + str(djeca[2]))
            return False
        
        else:
            print("POGREŠKA U <naredba_skoka>")
            return False
    
    elif(cvor.znak == "<prijevodna_jedinica>"):
        if(djeca[0].znak == "<vanjska_deklaracija>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
        
        elif(djeca[0].znak == "<prijevodna_jedinica>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not provjeri(djeca[1], tablica_IDN, djelokrug):
                return False
        
        else:
            print("POGREŠKA U <prijevodna_jedinica>")
            return False

    elif(cvor.znak == "<vanjska_deklaracija>"):
        if not provjeri(djeca[0], tablica_IDN, djelokrug):
            return False


    #TODO 4.4.6 Deklaracije i definicije
    elif(cvor.znak == "<definicija_funkcije>"):
        if(djeca[3].znak == "KR_VOID"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            #if not jeConstT(djeca[0].tip):

            if jeConstT(djeca[0].tip):
                print("<definicija_funkcije> ::= <ime_tipa> "+str(djeca[1])+" "+str(djeca[2])+" "+str(djeca[3])+" "+str(djeca[4])+" <slozena_naredba>")
                return False
            #mogu li dvije funkcije s istim imenima biti definirane u razlicitm djelokrugovima?
            #if (tablica_IDN[djeca[1].vrijednost].tip != None and isinstance(tablica_IDN[djeca[1].vrijednost].tip, Funkcija) and tablica_IDN[djeca[1].vrijednost].tip.definirana):
            if (djeca[1].vrijednost in tablica_IDN.keys() and isinstance(tablica_IDN[djeca[1].vrijednost].tip, Funkcija) and tablica_IDN[djeca[1].vrijednost].tip.definirana): 
                print("<definicija_funkcije> ::= <ime_tipa> "+str(djeca[1])+" "+str(djeca[2])+" "+str(djeca[3])+" "+str(djeca[4])+" <slozena_naredba>")
                return False  
            #if not (tablica_IDN[djeca[1].vrijednost].tip != None and isinstance(tablica_IDN[djeca[1].vrijednost].tip, Funkcija) and tablica_IDN[djeca[1].vrijednost].tip.params == "void" and tablica_IDN[djeca[1].vrijednost].tip.pov == djeca[0].tip):
            #if not (djeca[1].vrijednost in tablica_IDN.keys() and isinstance(tablica_IDN[djeca[1].vrijednost].tip, Funkcija) and tablica_IDN[djeca[1].vrijednost].tip.params == "void" and tablica_IDN[djeca[1].vrijednost].tip.pov == djeca[0].tip):
            if djeca[1].vrijednost in tablica_IDN.keys() and isinstance(tablica_IDN[djeca[1].vrijednost].tip, Funkcija) and not tablica_IDN[djeca[1].vrijednost].tip.definirana and not (tablica_IDN[djeca[1].vrijednost].tip.params == "void" and tablica_IDN[djeca[1].vrijednost].tip.pov == djeca[0].tip):
                print("<definicija_funkcije> ::= <ime_tipa> "+str(djeca[1])+" "+str(djeca[2])+" "+str(djeca[3])+" "+str(djeca[4])+" <slozena_naredba>")
                return False  
            
            
            #if tablica_IDN[djeca[1].vrijednost] == None:
            if not djeca[1].vrijednost in tablica_IDN.keys():
                tablica_IDN[djeca[1].vrijednost] =tablicaPodatak(Funkcija("void", djeca[0].tip, True), djelokrug[-1])
            else:
                tablica_IDN[djeca[1].vrijednost].tip.definirana = True
            
            if not provjeri(djeca[5], copy.deepcopy(tablica_IDN), djelokrug[:] + [djelokrugPodatak(Funkcija("void", djeca[0].tip), len(djelokrug)+1)]):
                return False
        
        elif(djeca[3].znak == "<lista_parametara>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if jeConstT(djeca[0].tip):
                print("<definicija_funkcije> ::= <ime_tipa> "+str(djeca[1])+" "+str(djeca[2])+" <lista_parametara> "+str(djeca[4])+" <slozena_naredba>")
                return False
            #if (tablica_IDN[djeca[1].vrijednost].tip != None and isinstance(tablica_IDN[djeca[1].vrijednost].tip, Funkcija) and tablica_IDN[djeca[1].vrijednost].tip.definirana): 
            if (djeca[1].vrijednost in tablica_IDN.keys() and isinstance(tablica_IDN[djeca[1].vrijednost], Funkcija) and tablica_IDN[djeca[1].vrijednost].definirana):
                print("<definicija_funkcije> ::= <ime_tipa> "+str(djeca[1])+" "+str(djeca[2])+" <lista_parametara> "+str(djeca[4])+" <slozena_naredba>")
                return False  
            if not provjeri(djeca[3], tablica_IDN, djelokrug):
                return False
            #if not (tablica_IDN[djeca[1].vrijednost].tip != None and isinstance(tablica_IDN[djeca[1].vrijednost].tip, Funkcija) and tablica_IDN[djeca[1].vrijednost].tip.params == djeca[3].tipovi and tablica_IDN[djeca[1].vrijednost].tip.pov == djeca[0].tip):
            if (djeca[1].vrijednost in tablica_IDN.keys() and isinstance(tablica_IDN[djeca[1].vrijednost].tip, Funkcija) and tablica_IDN[djeca[1].vrijednost].tip.params == djeca[3].tipovi and tablica_IDN[djeca[1].vrijednost].tip.pov == djeca[0].tip): 
                print("<definicija_funkcije> ::= <ime_tipa> "+str(djeca[1])+" "+str(djeca[2])+" <lista_parametara> "+str(djeca[4])+" <slozena_naredba>")
                return False  
            
            #if tablica_IDN[djeca[1].vrijednost] == None:
            if not djeca[1].vrijednost in tablica_IDN.keys():
                tablica_IDN[djeca[1].vrijednost] = tablicaPodatak(Funkcija(djeca[3].tipovi, djeca[0].tip, True), djelokrug[-1])
            else:
                tablica_IDN[djeca[1].vrijednost].tip.definirana = True
            
            #TODO MOZDA ZAJEBAJE
            novi_djelokrug = djelokrug[:] + [djelokrugPodatak(Funkcija(djeca[3].tipovi, djeca[0].tip), len(djelokrug)+1)]
            nova_tablica = copy.deepcopy(tablica_IDN) 
            for i in range(len(djeca[3].tipovi)):
                nova_tablica[djeca[3].imena[i]] = tablicaPodatak(djeca[3].tipovi[i], novi_djelokrug[-1])

            if not provjeri(djeca[5], nova_tablica, novi_djelokrug):
                return False
            

        else:
            print("POGREŠKA U <prijevodna_jedinica>")
            return False
        
    elif(cvor.znak == "<lista_parametara>"):
        if(djeca[0].znak  == "<deklaracija_parametra>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            cvor.tipovi = [ djeca[0].tip ]
            cvor.imena = [ djeca[0].ime ]
        
        elif(djeca[0].znak == "<lista_parametara>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            if djeca[2].ime in djeca[0].imena:
                print("<lista_parametara> ::= <lista_parametara> "+str(djeca[1])+" <deklaracija_parametra>")
                return False

            cvor.tipovi = djeca[0].tipovi + [ djeca[2].tip ]
            cvor.imena = djeca[0].imena + [ djeca[2].ime ]

        else:
            print("POGREŠKA U <lista_parametara>")
            return False
    
    elif(cvor.znak == "<deklaracija_parametra>"):
        if(len(djeca) == 2):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if djeca[0].tip == "void":
                print("<deklaracija_parametra> ::= <ime_tipa> " +str(djeca[1]))
                return False
            
            cvor.tip = djeca[0].tip
            cvor.ime = djeca[1].vrijednost
        
        elif(len(djeca) == 4):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if djeca[0].tip == "void":
                print("<deklaracija_parametra> ::= <ime_tipa> "+str(djeca[1])+" "+str(djeca[2])+" "+str(djeca[3]))
                return False
            
            cvor.tip = "niz(" + djeca[0].tip + ")"
            cvor.ime = djeca[1].vrijednost
        
        else:
            print("POGREŠKA U <deklaracija_parametra>")
            return False
    
    elif(cvor.znak == "<lista_deklaracija>"):
        if(djeca[0].znak == "<deklaracija>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug): 
                return False
        
        elif(djeca[1].znak == "<deklaracija>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not provjeri(djeca[1], tablica_IDN, djelokrug):
                return False

        else:
            print("POGREŠKA U <lista_deklaracija>")
            return False

    elif(cvor.znak == "<deklaracija>"):
        if(djeca[0].znak == "<ime_tipa>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug): 
                return False      
            
            djeca[1].ntip = djeca[0].tip

            if not provjeri(djeca[1], tablica_IDN, djelokrug):
                return False

        else:
            print("POGREŠKA U <deklaracija>")
            return False

    elif(cvor.znak == "<lista_init_deklaratora>"):
        if(djeca[0].znak == "<init_deklarator>"):
            djeca[0].ntip = cvor.ntip
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

        elif(djeca[0].znak == "<lista_init_deklaratora>"): #cudno je numerirano nesto u ovoj produkciji str 68 pa samo ostavljam natuknicu

            djeca[0].ntip = cvor.ntip
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            
            djeca[2].ntip = cvor.ntip
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
        
        else:
            print("POGREŠKA U <lista_init_deklaratora>")
            return False
    
    elif(cvor.znak == "<init_deklarator>"):
        if(len(djeca) == 1):
            djeca[0].ntip = cvor.ntip
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if jeConstT(djeca[0].tip) or jeNizConstT(djeca[0].tip):
                print("<init_deklarator> ::= <izravni_deklarator>")
                return False
    
        elif(len(djeca) == 3):
            djeca[0].ntip = cvor.ntip
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False

            if jeT(djeca[0].tip) or jeConstT(djeca[0].tip):
                #Marin promjena
                #print(djeca[0].tip, djeca[2].tip)
                #TODO ovo je sus (je li sukladno s uputama??)
                if not ImplicitnoXToY(djeca[2].tip, djeca[0].tip):
                    print("<init_deklarator> ::= <izravni_deklarator> "+str(djeca[1])+" <inicijalizator>")
                    return False
            elif jeNizT(djeca[0].tip) or jeNizConstT(djeca[0].tip):
                if not djeca[2].brelem <= djeca[0].brelem:
                    print("<init_deklarator> ::= <izravni_deklarator> "+str(djeca[1])+" <inicijalizator>")
                    return False 

                for tip in djeca[2].tipovi:
                    #if not ImplicitnoXToY(tip, djeca[0].tip)
                    if not ImplicitnoXToY(tip, "T"):
                        print("<init_deklarator> ::= <izravni_deklarator> "+str(djeca[1])+" <inicijalizator>")
                        return False 
            else:
                print("<init_deklarator> ::= <izravni_deklarator> "+str(djeca[1])+" <inicijalizator>")
                return False 
        
        else:
            print("POGREŠKA U <init_deklarator>")
            return False
    
    elif(cvor.znak == "<izravni_deklarator>"):
        if(len(djeca) == 1):
            #print(cvor.djeca, tablica_IDN, djelokrug)

            if cvor.ntip == "void":
                print("<izravni_deklarator> ::= "+str(djeca[0]))
                return False
            
            
            #if tablica_IDN[djeca[0].vrijednost] != None and tablica_IDN[djeca[0].vrijednost].djelokrug == djelokrug[-1]:
            #if djeca[0].vrijednost in tablica_IDN.keys():
            #    print(tablica_IDN[djeca[0].vrijednost].djelokrug, djelokrug[-1])
            
            if djeca[0].vrijednost in tablica_IDN.keys() and tablica_IDN[djeca[0].vrijednost].djelokrug == djelokrug[-1]:
                print("<izravni_deklarator> ::= "+str(djeca[0]))
                return False

            tablica_IDN[djeca[0].vrijednost] = tablicaPodatak(cvor.ntip, djelokrug[-1])

            cvor.tip = cvor.ntip

        elif(djeca[2].znak == "BROJ"):
            if cvor.ntip == "void":
                print("<izravni_deklarator> ::= "+str(djeca[0])+" "+str(djeca[1])+" "+str(djeca[2])+" "+str(djeca[3]))
                return False
            
            #if tablica_IDN[djeca[0].vrijednost] != None and tablica_IDN[djeca[0].vrijednost].djelokrug == djelokrug[-1]:
            if djeca[0].vrijednost in tablica_IDN.keys() and tablica_IDN[djeca[0].vrijednost].djelokrug == djelokrug[-1]:
                print("<izravni_deklarator> ::= "+str(djeca[0])+" "+str(djeca[1])+" "+str(djeca[2])+" "+str(djeca[3]))
                return False
            
            if not je1do1024(djeca[2].vrijednost):
                print("<izravni_deklarator> ::= "+str(djeca[0])+" "+str(djeca[1])+" "+str(djeca[2])+" "+str(djeca[3]))
                return False

            tablica_IDN[djeca[0].vrijednost] = tablicaPodatak("niz("+ cvor.ntip + ")", djelokrug[-1])
            cvor.tip = "niz("+ cvor.ntip + ")"
            cvor.brelem = int(djeca[2].vrijednost)


        elif(djeca[2].znak == "KR_VOID"):
            
            #if tablica_IDN[djeca[0].vrijednost] != None and tablica_IDN[djeca[0].vrijednost].djelokrug == djelokrug[-1] and not (tablica_IDN[djeca[0].vrijednost].tip.params == "void" and tablica_IDN[djeca[0].vrijednost].tip.pov == cvor.ntip):
            if djeca[0].vrijednost in tablica_IDN.keys() and tablica_IDN[djeca[0].vrijednost].djelokrug == djelokrug[-1] and not (tablica_IDN[djeca[0].vrijednost].tip.params == "void" and tablica_IDN[djeca[0].vrijednost].tip.pov == cvor.ntip):
                print("<izravni_deklarator> ::= "+str(djeca[0])+" "+str(djeca[1])+" "+str(djeca[2])+" "+str(djeca[3]))
                return False

            #if tablica_IDN[djeca[0].vrijednost] == None:
            if not djeca[0].vrijednost in tablica_IDN.keys():
                tablica_IDN[djeca[0].vrijednost] = tablicaPodatak(Funkcija("void", cvor.ntip), djelokrug[-1])

            cvor.tip = Funkcija("void", cvor.ntip)

        
        elif(djeca[2].znak == "<lista_parametara>"):
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False

            #if tablica_IDN[djeca[0].vrijednost] != None and tablica_IDN[djeca[0].vrijednost].djelokrug == djelokrug[-1]  and not (tablica_IDN[djeca[0].vrijednost].params == djeca[2].tipovi and tablica_IDN[djeca[0].vrijednost].pov == cvor.ntip):
            if djeca[0].vrijednost in tablica_IDN.keys() and tablica_IDN[djeca[0].vrijednost].djelokrug == djelokrug[-1]  and not (tablica_IDN[djeca[0].vrijednost].params == djeca[2].tipovi and tablica_IDN[djeca[0].vrijednost].pov == cvor.ntip):
                print("<izravni_deklarator> ::= "+str(djeca[0])+" "+str(djeca[1])+" "+str(djeca[2])+" "+str(djeca[3]))
                return False

            #if tablica_IDN[djeca[0].vrijednost] == None:
            if not djeca[0].vrijednost in tablica_IDN.keys() or djelokrug[-1] != tablica_IDN[djeca[0].vrijednost].djelokrug:
                tablica_IDN[djeca[0].vrijednost] = tablicaPodatak(Funkcija(djeca[2].tipovi, cvor.ntip), djelokrug[-1])
            #print(djeca[2].tipovi)
            cvor.tip = Funkcija(djeca[2].tipovi, cvor.ntip)

        else:
            print("POGREŠKA U <izravni_deklarator>")
            return False
    
    elif(cvor.znak == "<inicijalizator>"):
        if(djeca[0].znak == "<izraz_pridruzivanja>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False

            #---Nisam siguran za ovo---
            if djeca[0].tip == "niz(const(char))":
                #TODO ovo tu mozda nije dobro
                cvor.brelem = djeca[0].brelem + 1 
                cvor.tipovi = ["char" for i in range(cvor.brelem)]
            else:
                cvor.tip = djeca[0].tip
        
        elif(djeca[0].znak == "L_VIT_ZAGRADA"):
            if not provjeri(djeca[1], tablica_IDN, djelokrug):
                return False
            
            cvor.brelem = djeca[1].brelem
            cvor.tipovi = djeca[1].tipovi
        
        else:
            print("POGREŠKA U <inicijalizator>")
            return False
    elif(cvor.znak == "<lista_izraza_pridruzivanja>"):
        if(djeca[0].znak == "<izraz_pridruzivanja>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            cvor.tipovi = [djeca[0].tip]
            cvor.brelem = 1
        
        elif(djeca[0].znak == "<lista_izraza_pridruzivanja>"):
            if not provjeri(djeca[0], tablica_IDN, djelokrug):
                return False
            if not provjeri(djeca[2], tablica_IDN, djelokrug):
                return False
            cvor.tipovi = djeca[0].tipovi + [djeca[2].tip]
            cvor.brelem = djeca[0].brelem + 1         
        else:
            print("POGREŠKA U <lista_izraza_pridruzivanja>")
    else:
        print(djeca)
        print("NIJE PRONAĐENA PRODUKCIJA ZA: "+ str(cvor)) 
    
    if allDeclared:
        checkFunkcije(tablica_IDN, djelokrug)
    
    #whitespaces -=1
    return True

djelokrug = [djelokrugPodatak("GLOBAL", 1)]
golablni_djelokrug_IDN = dict()
if provjeri(korijen, golablni_djelokrug_IDN, djelokrug):
    zavrsnaProvjera(golablni_djelokrug_IDN, djelokrug)
    
