#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

def Add(addend1, addend2):
    return addend1 + addend2

def Subtract(num1, num2):
    return num1 - num2

def Multiply(factor1, factor2):
    return factor1 * factor2

def Divide(dividend, divisor):
    return dividend / divisor

def Exponent(num, exponent):
    return num ** exponent

def Abs(num):
    if num < 0:
        return -num
    else:
        return num

def ScientificNotation(num):
    revs = 0
    if num < 10 and num >= 0:
        return num
    elif num == 10:
        return "1x10^1"
    elif num > 10 or num < 0:
        if num >= 10:
            while num >= 10:
                num /= 10
                revs += 1
                return str(num) + "x10^" + str(revs)
        if num <= 0:
            while num <= 0:
                num /= -10
                revs += 1
            num /= -10
            revs += 1
            if num < 0:
                return str(num) + "x10^" + str(revs)
            else:
                return str(-num) + "x10^" + str(revs)