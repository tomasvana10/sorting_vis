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
button = ctk.CTkButton

# Constants limiting the min/max values of an array and how many elements in it
MINIMUM_ARRAY_VALUE = 1
MAXIMUM_ARRAY_VALUE = 1000
MINIMUM_ARRAY_SAMPLES = 1
MAXIMUM_ARRAY_SAMPLES = 600

# Append sorting times and function names from wrapper
sortingLog = []

def sortingTime(func: Callable[[list], list]) -> None:
    def wrapper(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        endTime = time.time()
        sortingLog.append(
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
        self.titleLabel = ctk.CTkLabel(self,
            text="Sorting Algorithm Visualisation",
            font=ctk.CTkFont(family="Courier New",
                             size=25, weight="bold"))
        self.sortingImage = ctk.CTkLabel(self, text="", 
            image=ctk.CTkImage(Image.open(
            "assets/sorting_vis.png"),
            size=(300,150)))
        # Get all func names (sorting functions) except __init__
        self.availableSortingFunctions = ["bubbleSort", "insertionSort",
                                          "selectionSort"]
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
        self.clearEntriesButton = ctk.CTkButton(self, text="Clear inputs", 
            font=self.defaultFont, command=self.clearEntries)
        self.fillMaxValuesButton = ctk.CTkButton(self, 
            text="Fill in max array values", font=self.defaultFont, 
            command=self.fillMaxValues)
        
        self.titleLabel.place(relx=0.5, rely=0.415, anchor="c")
        self.sortingImage.place(relx=0.5, rely=0.1925, anchor="c")
        self.chooseAlgorithm.place(relx=0.3, rely=0.6, anchor="c")
        self.chooseAlgorithmLabel.place(relx=0.3, rely=0.55, anchor="c")
        self.lowerSampleBoundEntry.place(relx=0.7, rely=0.6, anchor="c")
        self.upperSampleBoundEntry.place(relx=0.7, rely=0.725, anchor="c")
        self.lowerSampleBoundLabel.place(relx=0.7, rely=0.55, anchor="c")
        self.upperSampleBoundLabel.place(relx=0.7, rely=0.675, anchor="c")
        self.sampleCountEntry.place(relx=0.3, rely=0.725, anchor="c")
        self.sampleCountEntryLabel.place(relx=0.3, rely=0.675, anchor="c")
        self.openSorterButton.place(relx=0.7, rely=0.925, anchor="c")
        self.randomEntryFillButton.place(relx=0.3, rely=0.825, anchor="c")
        self.clearEntriesButton.place(relx=0.7, rely=0.825, anchor="c")
        self.fillMaxValuesButton.place(relx=0.3, rely=0.925, anchor="c")

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
            self.arrayVisualiser = ArrayVisualiser(self, self.lowerInput, 
                self.upperInput, self.sampleCountInput,
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
            f"{random.randint(MINIMUM_ARRAY_VALUE, int(MAXIMUM_ARRAY_VALUE / 2))}")
        self.upperSampleBoundEntry.insert(0,
            f"{random.randint(int(self.lowerSampleBoundEntry.get()) + 1, MAXIMUM_ARRAY_VALUE)}")
        self.sampleCountEntry.insert(0, 
            f"{random.randint(MINIMUM_ARRAY_SAMPLES, MAXIMUM_ARRAY_SAMPLES)}")

    def fillMaxValues(self) -> None:
        self.clearEntries()
        self.lowerSampleBoundEntry.insert(0, 1)
        self.upperSampleBoundEntry.insert(0, MAXIMUM_ARRAY_VALUE)
        self.sampleCountEntry.insert(0, MAXIMUM_ARRAY_SAMPLES)


class ArrayVisualiser(ctk.CTkToplevel):
    def __init__(self, master: HomeScreen, lowerbound: int, upperbound: int, 
            samplecount: int, algorithm: str) -> None:
        super().__init__(master)
        self.title(algorithm)
        self.geometry(f"{self.master.scnWidth}x{self.master.scnHeight}")
        ctk.set_widget_scaling(0.9)
        self.master = master
        self.LOWERBOUND = lowerbound
        self.UPPERBOUND = upperbound
        self.SAMPLECOUNT = samplecount
        self.ALGORITHM = algorithm
        # This instance will have all the sorting algorithm methods
        self.sorter = SortingAlgorithms(self) 
        self.isCurrentlySorting = False
        self.makeContent()
        # Display array to user
        self.arraySetup()
        
    def makeContent(self) -> None:
        self.frame = ctk.CTkFrame(self)
        self.initialiseSortButton = ctk.CTkButton(self.frame, 
            text="Initialise sort", font=self.master.defaultFont, 
            command=lambda: self.initialiseSort(self.arr), state="disabled")
        self.generateNewArrayButton = ctk.CTkButton(self.frame, 
            text="Make a new array", font=self.master.defaultFont,
            command=self.arraySetup)
        self.startOrStopSortButton = ctk.CTkButton(self.frame,
            text="Stop sorting", font=self.master.defaultFont,
            state="disabled", command=self.startOrStopSort)
        self.canvas = tk.Canvas(self.frame, width=self.master.scnWidth - 60,
            height=self.master.scnHeight * 0.9 - 60, background="#2d4485")
    
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.initialiseSortButton.place(relx=0.4, rely=0.95, anchor="c")
        self.generateNewArrayButton.place(relx=0.5, rely=0.95, anchor="c")
        self.startOrStopSortButton.place(relx=0.6, rely=0.95, anchor="c")
        self.canvas.pack(padx=30, pady=(30, 78))

    def arraySetup(self) -> None:
        self.isCurrentlySorting = False
        self.startOrStopSortButton.configure(state="disabled", 
            text="Stop sorting")
        self.initialiseSortButton.configure(state="normal")
        
        self.arr = list(np.random.randint(self.LOWERBOUND, self.UPPERBOUND, 
            self.SAMPLECOUNT))
        self.ARRLENGTH = len(self.arr)
        self.MINVAL = np.min(self.arr)
        self.MAXVAL = np.max(self.arr)
        self.RANGE = self.MAXVAL - self.MINVAL
        self.renderArray(self.arr)

    def initialiseSort(self, arr: list[int]) -> None:
        self.isCurrentlySorting = True
        self.sorter.pauseSort = False
        self.startOrStopSortButton.configure(state="normal")
        self.initialiseSortButton.configure(state="disabled")
        self.generateNewArrayButton.configure(state="disabled")
        
        if self.ALGORITHM == "bubbleSort":
            self.sorter.bubbleSort(arr)
        elif self.ALGORITHM == "selectionSort":
            self.sorter.selectionSort(arr)
        elif self.ALGORITHM == "insertionSort":
            self.sorter.insertionSort(arr)

    def startOrStopSort(self) -> None:
        if self.isCurrentlySorting:
            self.sorter.pauseSort = True
            self.isCurrentlySorting = False
            self.startOrStopSortButton.configure(text="Start Sorting", 
                state="normal")
            self.generateNewArrayButton.configure(state="normal")
        else:
            self.sorter.pauseSort = False
            self.isCurrentlySorting = True 
            self.startOrStopSortButton.configure(text="Stop Sorting", 
                state="normal")
            self.generateNewArrayButton.configure(state="disabled")
            self.initialiseSort(self.sorter.pausedArray)

    def renderArray(self, arr: list[int], sortingidxs: list[int] = [], 
            complete: bool = False) -> None:
        # sortingidxs refer to the two (or more with some sorts) indexes that
        # are currently being modified
        
        self.canvas.delete("columns")
        canvasWidth = self.canvas.winfo_reqwidth() - 10
        canvasHeight = self.canvas.winfo_reqheight() - 21
        barWidth = canvasWidth / self.ARRLENGTH

        for i, item in enumerate(arr):
            x1 = i * barWidth + 3
            y1 = canvasHeight * (1 - (item - self.MINVAL) / self.RANGE)
            x2 = x1 + barWidth
            y2 = canvasHeight
            if not complete:    
                fill = "#eb3f3f" if i in sortingidxs else "#aebac2"
                outline = "#eb6e6e" if i in sortingidxs else "#c7cdd1"
            else:
                fill = "#34eb55"
                outline = "#86eb98"
            
            self.canvas.create_rectangle(x1, y1, x2, y2, 
                fill=fill, outline=outline, tags="columns")
        if complete:
            self.isCurrentlySorting = False
            self.startOrStopSortButton.configure(state="disabled")
            self.generateNewArrayButton.configure(state="normal")
        
        self.update()
        

class SortingAlgorithms:
    def __init__(self, master) -> None:
        self.master = master
        self.pauseSort = False
        self.pausedArray = []
        
    @sortingTime
    def bubbleSort(self, arr: list[int]) -> None:
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
                    if self.pauseSort:
                        self.pausedArray = arr.copy()
                        return 
                    self.master.renderArray(arr, [j, j+1])
        self.master.renderArray(arr, complete=True)
    
    @sortingTime
    def selectionSort(self, arr: list[int]) -> None: 
        '''Iterate through an array, with each new iteration excluding another 
        item from the start of the list. Each iteration finds the smallest 
        item in the array and switches it with the next item of the outer loop.
        '''
        length = len(arr)
        for i in range(length):
            minIndex = i # Assume minIndex is iterator i
            for j in range(i, length):
                if arr[j] < arr[minIndex]: 
                    minIndex = j
            if minIndex != i: 
                arr[i], arr[minIndex] = arr[minIndex], arr[i]
                if self.pauseSort:
                        self.pausedArray = arr.copy()
                        return
                self.master.renderArray(arr, [i, minIndex])
        self.master.renderArray(arr, complete=True)

    @sortingTime
    def insertionSort(self, arr: list[int]) -> None:
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
                if self.pauseSort:
                        self.pausedArray = arr.copy()
                        return
                self.master.renderArray(arr, [j, j-1])
                j -= 1 
        self.master.renderArray(arr, complete=True)
        return arr
    
    
if __name__ == "__main__":
    app = HomeScreen()
    app.mainloop()