from Levenshtein import distance

class Spell_checker:
    def __init__(self):
        self.spanish_dict = self._load_dict('./diccionario_espanol.txt')
        self.slang_dict = self._load_jergas('./jergas_español.txt')

    def _load_dict(self, route):
        dictionary = {}
        with open(route, encoding="utf8") as words:
            aux = words.read().split()
        for i in range(len(aux)):
            dictionary[aux[i]] = 1
        return dictionary

    def _load_jergas(self, route):
        dictionary = {}
        with open(route, encoding="utf8") as words:
            aux = words.read().split('\n')
            for i in range(len(aux)-1):
                tmp = aux[i].split(";")
                dictionary[tmp[0]] = tmp[1]
        return dictionary


    def get_correction(self, word):
      return min(self.spanish_dict, key=lambda x: distance(word, x))

    def filter(self, string):
        result = ""
        for word in string.split():
            #Conectores
            if len(word) <= 1:
                result+=word
                continue
            #Nombres propios o de lugares
            if word[0].isupper():
                result+=' '+word
                continue
            if len(word) >= 1:
                #Si es un hashtag
                if word[0] == "#":
                    aux = ""
                    for char in word:
                        #Separar "#"
                        if char == "#":
                            pass
                        elif char.isupper() and aux != "":
                            #Si esta en nuestro diccionario
                            if aux in self.spanish_dict:
                                result+= " " + aux
                                aux = ""
                            #O si es una jerga
                            elif aux in self.slang_dict:
                                result+=" " + self.slang_dict[aux]
                                aux = ""
                            #if, by discarting we concluded that the word could be misspelled, then apply a levenshtein distance:
                            else:
                                if len(word) > 3:
                                    result+=" " + self.get_correction(word)
                                else:
                                    result+=" " + word

                                aux=char.lower()
                        else:
                            aux+=char.lower()
                    word = aux
                #Nombre de usuario, quitar "@"
                elif word[0] == "@":
                    result+=" "+ word[1:-1]
                    continue
            #Quitar links
            if len(word) >= 5 and word[0:5] == "https":
                continue

            #Checar que este en el diccionario
            if word.lower() in self.spanish_dict:
                result+= " " + word.lower()

            #Si es una jerga
            elif word.lower() in self.slang_dict:
                result+=" " + self.slang_dict[word.lower()]
            #Checar si la palabra esta escrita incorrectamente
            else:
                if len(word) > 3:
                    result+=" " + self.get_correction(word)
                else:
                    result+=" " + word
        return result
