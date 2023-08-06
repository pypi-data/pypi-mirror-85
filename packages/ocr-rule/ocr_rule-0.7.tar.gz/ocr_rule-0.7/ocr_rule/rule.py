import re 


class Idcard_Indonesia(): 
    def __init__(self): 
        self.NAME_FLAG = ["Nama", "Nam", "Iama", "Lama", "lama", "Vama", "vama"] 
        self.GENDER_FLAG = ["PEREMPUAN", " PEREMPUAN", "EREMPUAN", "PEREMPUA", "FEMALE"]
        self.KEY = []


    def __get_ic(self, text_list): 
        ic_number = "-"
        get_ic = False

        for i in text_list: 
            if re.match(r'^([\s\d]+)$', i): 
                ic_number = i 
                get_ic = True
                break
        return ic_number, get_ic

    
    def __get_name(self, text_list): 
        name = "-"
        get_name = False

        for idx, i in enumerate(text_list): 
            if i in self.NAME_FLAG: 
                name = text_list[idx + 1]
                if bool(re.match('[A-Z ]+$', name)) \
                    and not(bool(re.search(r'\d', name))): 
                    get_name = True
                    break
                else: 
                    name = text_list[idx + 2]
                    if (bool(re.match('[A-Z ]+$', name))) \
                        and not(bool(re.search(r'\d', name))): 
                        get_name = True
                        break
                    else: 
                        name = text_list[max(0, idx - 1)]
                        if (bool(re.match('[A-Z ]+$', name)))\
                             and not(bool(re.search(r'\d', name))): 
                            get_name = True
                            break
                        else: 
                            name = "-"
                    
        return name, get_name

    
    def __get_dob(self, text_list): 
        dob = "-"
        get_dob = False

        for idx, i in enumerate(text_list): 
            pos_dob = re.findall("\d{1,2}-\d{1,2}-\d{4}", i)
            if len(pos_dob) > 0 and not(get_dob): 
                dob = pos_dob[0]
                dob = dob.replace(" ", "")
                get_dob = True

        return dob, get_dob

    
    def __get_address(self, text_list): 
        address = "-"
        get_address = False 

        if ("KAB" in text_list[1] \
            or "ABUP" in text_list[1]
            or "OTA" in text_list[1]) \
            and "PROV" in text_list[0]: 
            get_address = True
            address = text_list[1] + " " + text_list[0]
        return address, get_address


    def __get_gender(self, text_list): 
        gender = "-"
        get_gender = False

        for idx, i in enumerate(text_list): 
            if bool(re.match('[A-Z- ]+$', i)): 
                if bool(re.match("[A-Z ]{2,4}I-L[A-Z ]{2,4}", i)) or i =="MALE":
                    gender = "M"
                    get_gender = True
                    break
                elif i in self.GENDER_FLAG: 
                    gender = "F"
                    get_gender = True
                    break
        return gender, get_gender


    def process(self, text_list): 
        name, get_name = self.__get_name(text_list)
        num_ic, get_ic = self.__get_ic(text_list)
        dob, get_dob = self.__get_dob(text_list)
        gender, get_gender = self.__get_gender(text_list)
        address, get_address = self.__get_address(text_list)
        state = "-"

        result = {"ic_number": num_ic, "name": name, 
                  "gender": gender, "dob": dob, 
                  "address": address, "state": state}
        print (result)
        return result



class Idcard_Malaysia(): 
    def __init__(self): 
        self.MY_REGION_LIST = ['KUALA LUMPUR','KUALA ', 
                                'W.P. KUALA LUMPUR', "W. PERSEKUTUAN(KL)",
                                'W. PERSEKUTUANIKL)', 'W. PERSEKUTUAN(KL', 
                                'W. PERSEKUTUANIKL', 'W PERSEKUTUAN(KL)',
                                'JOHOR', "KEDAH", "PERAK", "PAHANG", "PERSEKUTUAN",
                                "SABAH", "SELANGOR", "SARAWAK", "TERENGGANU", 
                                "KELANTAN", "PULAU PINANG", "MELAKA", 
                                "NEGERI SEMBILAN", "PERLIS", "LABUAN"]


    def __get_ic(self, text_list): 
        selected_ic = '-'
        ic_index = None
        get = False

        for idx, i in enumerate(text_list): 
            if len(i.split('-')) == 3:
                selected_ic = re.sub('\D', '', i)
                ic_index = idx
                get = True 
                break

        return selected_ic, ic_index, get


    def __get_dob(self, ic_number):
        year = int(ic_number[:2])
        month = ic_number[2:4]
        day = ic_number[4:6]
        actualyear = year

        if year >= 50:
            actualyear = actualyear + 1900
        else:
            actualyear = actualyear + 2000

        return day+'-'+month+'-'+ str(actualyear)


    def __get_gender(self, ic_number):
        last_digit = int(ic_number[-1])
        if last_digit%2 == 0:
            return 'F'
        else:
            return 'M'

    
    def __get_address(self, text_list):
        """[summary]
        Arguments:
            response {[type]} -- [description]
        Returns:
            [type] -- [description]
        """    
        address = ''
        state = ''

        for idx, i in enumerate(text_list): 
            if i in self.MY_REGION_LIST: 
                address = text_list[idx -5] + " " + text_list[idx-4] + " " + text_list[idx-3] + " " + text_list[idx-2]
                state = i
                break

        return address, state

    
    def __get_fullname(self, text_list, ic_index):
        """[summary]
        Arguments:
            response {[type]} -- [description]
            ic_index {[type]} -- [description]
        Returns:
            [type] -- [description]
        """    
        selected_name = ''

        for idx, i in enumerate(text_list): 
            if idx > ic_index: 
                suku_kata = i.split(" ")

                if len(suku_kata) >= 2 or ('BIN' in i or "Bin" in i or "BINTI" in i or "Binti" in i): 
                    selected_name = i
                    break

        return selected_name

    
    def process(self, text_list): 
        ic_number, ic_index, get_ic = self.__get_ic(text_list)
        full_name = '-' 
        gender = '-'
        dob = '-'
        address = '-'
        state = '-'

        if get_ic: 
            print (ic_number)
            full_name = self.__get_fullname(text_list, ic_index)
            print (full_name)
            gender = self.__get_gender(ic_number)
            print (gender)
            dob = self.__get_dob(ic_number)
            print (dob)
            address, state = self.__get_address(text_list)
            print (address)
        
        result = {"ic_number": ic_number, "name": full_name, 
                  "gender": gender, "dob": dob, 
                  "address": address, "state": state}
        return result



class Idcard_Singapore(): 
    def __init__(self): 
        a = None 

    
    def process(self, text_list): 
        name = "-" 
        num_ic = "-" 
        dob = "-"
        gender = "-"
        address = "-"
        state = "-"

        for idx, i in enumerate(text_list): 
            if "Nama" in i or "Name" in i or "Nam" in i or "ame" in i: 
                name = text_list[idx + 1]
                if not(bool(re.match('[A-Z ,()]+$', name))): 
                    name = "-"

            if bool(re.search("(s|S)(\d){7}", i)): 
                num_ic = i.split(" ")[-1]

            tmp_dob = re.findall("\d{1,2}-\d{1,2}-\d{3,4}", i)
            if len(tmp_dob) > 0: 
                dob = tmp_dob[0]

            if i == "M" or i == "F": 
                gender = i

        print (name)
        print (num_ic) 
        print (dob)
        print (gender)

        result = {"ic_number": num_ic, "name": name, 
                  "gender": gender, "dob": dob, 
                  "address": address, "state": state}
        return result


class Idcard_Vietnam(): 
    def __init__(self): 
        self.DOB_CHARS = ["Sinh ngay", "Sinh ingay", 
                            "Sinh nga", "Sin ingay", 
                            "inh ngay"]

    def process(self, text_list): 
        name = "-"
        num_ic = "-"
        dob = "-"
        gender = "-"
        address = "-"
        state = "-"

        for idx, i in enumerate(text_list): 
            if  ("Ho ten" in i or "Ho te" in i \
                or "o ten" in i or "Hot" in i \
                or "Ho t" in i or "Ho" in i) and len(i) <= 6: 
                name = text_list[idx + 1]

            tmp_dob = re.findall("\d{1,2}-\d{1,2}-\d{3,4}", i)
            if len(tmp_dob) > 0: 
                dob = tmp_dob[0]
            else: 
                tmp_dob = re.findall("\d{1,2}/\d{1,2}/\d{3,4}", i)
                if len(tmp_dob) > 0: 
                    dob = tmp_dob[0]

            if "Nguyen quan" in i or "quan" in i or "Nguyen " in i: 
                address = text_list[idx + 1] + ", " + text_list[idx + 2]

        print (name)
        print (num_ic)
        print (dob)
        print (gender)
        print (address)
        print (state)
        result = {"ic_number": num_ic, "name": name, 
                  "gender": gender, "dob": dob, 
                  "address": address, "state": state}
        return result



class Idcard_Thailand(): 
    def __init__(self): 
        a = None 

    
    def process(self, text_list): 
        name = "-"
        num_ic = text_list[1]
        dob = "-"
        gender = "-"
        address = "-"
        state = "-"
        get_dob = False

        for idx, i in enumerate(text_list): 
            if "Name" in i or "Nam" in i \
                or "Neme" in i: 
                name = i.split(" ")[-1]
                if "Miss" in i or "Mrs" in i \
                    or "Mis" in i: 
                    gender = 'F'
                elif "Mr" in i: 
                    gender = "M"

            if "Last name" in i or "Last nam" in i \
                or "ast nam" in i or "Last" in i: 
                name = name + " " + i.split(" ")[-1]
            
            tmp_dob= re.findall("\d{1,2} [A-Za-z]{3}. \d{3,4}", i)
            if len(tmp_dob) and not(get_dob): 
                dob = tmp_dob[0]
                get_dob = True

        print (name)
        print (num_ic)
        print (dob)
        print (gender)
        print (address)
        print (state)

        result = {"ic_number": num_ic, "name": name, 
                  "gender": gender, "dob": dob, 
                  "address": address, "state": state}

        return result 
        
