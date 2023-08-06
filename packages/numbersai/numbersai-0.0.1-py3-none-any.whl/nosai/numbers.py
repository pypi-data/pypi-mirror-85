"""
1999- Nineteen Ninty Nine
1888 - Eighteen Eighty Eight
1777 - Seventeen Seventy Seven
1111 - Oneeen Onety One

Not fully huristics
"""

from num2words import num2words

def spell(N):
    if N // 1_0000 ==0:
        N = divmod(N, 100)
        top, bot = N[0], N[1]

        result = [ ]

        if top == 11:
            result.append("OneTeen")
        elif top == 12:
            result.append("TwoTeen")

        else:
            result.append(num2words(top))


        botx, boty = divmod(bot, 10)

        if botx == 1:
            result.append("Onety")
            result.append(num2words(boty))

        else:
            result.append(num2words(bot))

        return ' '.join(result)

