"""lz77"""

def find_second_last_occurrence(string, str_to_find):
    """Допоміжна функція для знаходження офсету, знаходить 2ге з кінця входження значення"""
    # Знаходимо всі індекси, де починається підрядок
    indices = [i for i in range(len(string) - len(str_to_find) + 1) \
if string.startswith(str_to_find, i)]
    # Якщо знайдено 2 або більше входження, повертаємо передостаннє
    if len(indices) >= 2:
        return indices[-2]
    else:
        return -1

def codding(text, buffer_lengh=5):
    """lz77 закодування"""
    all_text = text
    result, buffer = [], []
    ofset, lenght, nexxt = 0, 0, ''
    ind = 0
    while text:
        if all_text[ind] in buffer:
            buffer_lenght_befor = len(buffer) #якщо буфер ще не заповнений повністю
            ofset = buffer_lenght_befor - ''.join(buffer).rfind(all_text[ind])
            buffer.append(all_text[ind][-1]) #щоб цей прикол з повторами одразу ловити
            text = text[1:]
            matched = all_text[ind] #ця літера є, того змечили її
            for i, el in enumerate(text): #Шукаємо найкращий метч
                if matched+el in "".join(buffer):
                    matched += el
                    buffer.append(el)
                else:
                    buffer.append(el)
                    # ofset = ''.join(buffer).rfind(matched) - ''.join(buffer).find(matched)
                    ofset = ''.join(buffer).rfind(matched) - \
                        find_second_last_occurrence(''.join(buffer), matched)
                    #на випадок, що в нас було кілька варіантів "початку", але обираємо той,
                    # що дозволяє за один раз більше закодити
                    if len(buffer) > buffer_lengh:
                        buffer = buffer[-buffer_lengh:]
                    lenght, nexxt = len(matched), el
                    nexxt = el
                    if i == len(text) - 1:
                        nexxt = " "
                    text = text[len(matched):]
                    result.append((ofset, lenght, nexxt))
                    ind += len(matched) +1
                    # print(result[-1], text)
                    break
        else: #випадок першого входження літери
            buffer.append(all_text[ind])
            ofset, lenght, nexxt = 0, 0, all_text[ind]
            result.append((ofset, lenght, nexxt))
            text = text[1:]
            if len(buffer) > buffer_lengh:
                buffer = buffer[-buffer_lengh:]
            ind += 1
            # print(result[-1], text)
    # print(text)
    return result


def decoding(codded):
    """Алгоритм декожування до lz77"""
    result = []
    for el in codded:
        ofset, lenght, neext = el
        if ofset == 0: #перше входження літери
            result.append(neext)
        elif ofset == lenght: #звичайний випадок
            result.append(''.join(result)[-ofset:] + neext)
        elif ofset > lenght: #звичайний випадок
            result.append(''.join(result)[-ofset:-ofset+lenght] + neext)
        else: #ця наша найприкріша ситуація
            timed = "".join(result)[-ofset]*(lenght//ofset)
            timed += timed[:-(lenght%ofset)] + neext
            result.append(timed)
        # print(result)
    # print(result)
    result = "".join(result)
    # print(result)
    return result

if __name__=='__main__':
    our_text = 'Карл у Клари украв коралі, а Клара у Карла вкрала кларнет'
    print(codding(our_text))
    codded = codding(our_text)
    print(decoding(codded))
    print(our_text == decoding(codded))
