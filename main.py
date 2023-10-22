'''A customtkinter gui that utilises various sorting algorithms to visualise
how an array is sorted
'''

import time
import math
import numpy as np
import tkinter as tk
import tkinter.messagebox
from PIL import Image
from typing import Callable
import inspect
import os
import random

import customtkinter as ctk

MINIMUM_ARRAY_VALUE = 1
MAXIMUM_ARRAY_VALUE = 400
MINIMUM_ARRAY_SAMPLES = 5
MAXIMUM_ARRAY_SAMPLES = 350

sorting_log = []

def sortingTime(func: Callable[[list], list]) -> None:
    def wrapper(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        endTime = time.time()
        sorting_log.append(
            {"name": func.__name__,
             "runtime": endTime-startTime})
        return result
    return wrapper


class HomeScreen(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Sorting Algorithm Visualisation")
        self.geometry("500x500")
        self.minsize(500, 500)
        ctk.set_widget_scaling(0.9)
        ctk.set_default_color_theme(
            "assets/themes/TrojanBlue.json")
        self.defaultFont = ctk.CTkFont(family="Courier New")
        self.scnWidth = self.winfo_screenwidth()
        self.scnHeight = self.winfo_screenheight()
        self.makeContent()
        
    def makeContent(self) -> None:
        # Widgets
        self.titleLabel = ctk.CTkLabel(self,
            text="Sorting Algorithm Visualisation",
            font=ctk.CTkFont(family="Courier New",
                             size=25, weight="bold"))
        self.sortingImage = ctk.CTkLabel(self, text="", 
            image=ctk.CTkImage(Image.open(
            "assets/sorting_vis.png"),
            size=(300,150)))
        self.availableSortingFunctions = [
            method[0] for method in inspect.getmembers(SortingAlgorithms) 
            if inspect.isfunction(method[1])]
        self.chooseAlgorithm = ctk.CTkOptionMenu(self, 
            values=self.availableSortingFunctions, font=self.defaultFont)
        self.chooseAlgorithmLabel = ctk.CTkLabel(self, 
            text="Sorting algorithm",
            font=self.defaultFont)
        self.lowerSampleBoundEntry = ctk.CTkEntry(self, 
            placeholder_text=f"< upper, >= {MINIMUM_ARRAY_VALUE}",
            font=self.defaultFont)
        self.upperSampleBoundEntry = ctk.CTkEntry(self,
            placeholder_text=f"> lower, <= {MAXIMUM_ARRAY_VALUE}",
            font=self.defaultFont)
        self.lowerSampleBoundLabel = ctk.CTkLabel(self,
            text="Lower sample bound", font=self.defaultFont)
        self.upperSampleBoundLabel = ctk.CTkLabel(self,
            text="Upper sample bound", font=self.defaultFont)
        self.sampleCountEntry = ctk.CTkEntry(self, 
            placeholder_text=(
                f">= {MINIMUM_ARRAY_SAMPLES}, <= {MAXIMUM_ARRAY_SAMPLES}"),
            font=self.defaultFont)
        self.sampleCountEntryLabel = ctk.CTkLabel(self, text="Sample count",
            font=self.defaultFont)
        self.openSorterButton = ctk.CTkButton(self, text="Load array", 
            font=self.defaultFont, command=self.loadArray)
        self.randomEntryFillButton = ctk.CTkButton(self,
            text="Randomly fill inputs", 
            font=self.defaultFont, command=self.randomEntryFiller)
        self.clearEntriesButton = ctk.CTkButton(self, text="Clear entries", 
            font=self.defaultFont, command=self.clearEntries)
        
        
        # Placing
        self.titleLabel.place(relx=0.5, rely=0.415, anchor="c")
        self.sortingImage.place(relx=0.5, rely=0.195, anchor="c")
        self.chooseAlgorithm.place(relx=0.3, rely=0.6, anchor="c")
        self.chooseAlgorithmLabel.place(relx=0.3, rely=0.55, anchor="c")
        self.lowerSampleBoundEntry.place(relx=0.7, rely=0.6, anchor="c")
        self.upperSampleBoundEntry.place(relx=0.7, rely=0.725, anchor="c")
        self.lowerSampleBoundLabel.place(relx=0.7, rely=0.55, anchor="c")
        self.upperSampleBoundLabel.place(relx=0.7, rely=0.675, anchor="c")
        self.sampleCountEntry.place(relx=0.3, rely=0.725, anchor="c")
        self.sampleCountEntryLabel.place(relx=0.3, rely=0.675, anchor="c")
        self.openSorterButton.place(relx=0.5, rely=0.925, anchor="c")
        self.randomEntryFillButton.place(relx=0.3, rely=0.825, anchor="c")
        self.clearEntriesButton.place(relx=0.7, rely=0.825, anchor="c")

    def checkValidEntries(self) -> bool:
        try:
            self.lowerInput = int(self.lowerSampleBoundEntry.get())
            self.upperInput = int(self.upperSampleBoundEntry.get())
            self.sampleCountInput = int(self.sampleCountEntry.get())
        except:
            tk.messagebox.showerror(message="Entries have non-integer inputs! \
                Press Enter to continue.")
            return False

        if (self.lowerInput < MINIMUM_ARRAY_VALUE 
                or self.upperInput > MAXIMUM_ARRAY_VALUE
                or self.lowerInput >= self.upperInput 
                or self.sampleCountInput > MAXIMUM_ARRAY_SAMPLES
                or self.sampleCountInput < MINIMUM_ARRAY_SAMPLES):
            tk.messagebox.showerror(
                message="Entries must contain integers within the required \
                    bounds! Press Enter to continue.")
            return False
        else:
            return True
            
    def loadArray(self) -> None:
        if self.checkValidEntries():
            self.arrayVisualiser = ArrayVisualiser(self, 
                self.lowerInput, self.upperInput, self.sampleCountInput,
                self.chooseAlgorithm.get())
            return

    def clearEntries(self) -> None:
        self.lowerSampleBoundEntry.delete(0, tk.END)
        self.upperSampleBoundEntry.delete(0, tk.END)
        self.sampleCountEntry.delete(0, tk.END)
        self.lowerSampleBoundEntry.focus()
        self.upperSampleBoundEntry.focus()
        self.sampleCountEntry.focus()
        self.focus()

    def randomEntryFiller(self) -> None:
        self.clearEntries()
        self.lowerSampleBoundEntry.insert(0, 
            f"{random.randint(MINIMUM_ARRAY_VALUE, int(MAXIMUM_ARRAY_VALUE/2))}")
        self.upperSampleBoundEntry.insert(0,
            f"{random.randint(int(self.lowerSampleBoundEntry.get()), MAXIMUM_ARRAY_VALUE)}")
        self.sampleCountEntry.insert(0, 
            f"{random.randint(MINIMUM_ARRAY_SAMPLES, MAXIMUM_ARRAY_SAMPLES)}")

class ArrayVisualiser(ctk.CTkToplevel):
    def __init__(self, master, lowerbound, upperbound, samplecount,
            algorithm) -> None:
        super().__init__(master)
        self.title(algorithm)
        self.geometry(f"{self.master.scnWidth}x{self.master.scnHeight}")
        ctk.set_widget_scaling(0.9)
        ctk.set_default_color_theme(
            "sorting_algorithms_app/assets/themes/TrojanBlue.json")
        self.master = master
        self.LOWERBOUND = lowerbound
        self.UPPERBOUND = upperbound
        self.SAMPLECOUNT = samplecount
        self.ALGORITHM = algorithm
        self.makeContent()
    
    def makeContent(self):
        # Widgets
        ...
    
    



class SortingAlgorithms:
    @staticmethod
    @sortingTime
    def bubbleSort(arr: list[int | float]) -> list[int | float]:
        '''Iterate through an array, where each iteration excludes another 
        item from the end. With each iteration, arr[j] and arr[j+1] are 
        compared. If arr[j] is greater than arr[j+1], they switch. Say arr[j] 
        is the greatest value in the array, then with each iteration it will 
        switch with the value to its right, effectively "bubbling" to the end 
        of the array.
        '''
        length = len(arr)
        for i in range(length):
            for j in range(length-i-1): 
                if arr[j] > arr[j+1]: 
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    @staticmethod
    @sortingTime
    def selectionSort(arr: list[int | float]) -> list[int | float]: 
        '''Iterate through an array, with each new iteration excluding another 
        item from the start of the list. Each iteration finds the smallest 
        item in the array and switches it with the next item of the outer loop.
        '''
        length = len(arr)
        for i in range(length):
            minIndex = i # Assume minIndex is the current outer iterator
            for j in range(i, length):
                if arr[j] < arr[minIndex]: 
                    minIndex = j
            if minIndex != i: 
                arr[i], arr[minIndex] = arr[minIndex], arr[i]
        return arr

    @staticmethod
    @sortingTime
    def insertionSort(arr: list[int | float]) -> list[int | float]:
        '''Similar to bubble sort but in reverse. The insertion sort algorithm
        selects an item in an array and shifts it to the left (descending)
        until the value to its left is smaller than it. This process builds
        the sorted array from the left to the right.
        '''
        length = len(arr)
        for i in range(1, length): 
            j = i
            while j > 0 and arr[j-1] > arr[j]: 
                arr[j], arr[j-1] = arr[j-1], arr[j]
                j -= 1 
        return arr
    
    
if __name__ == "__main__":
    app = HomeScreen()
    app.mainloop()