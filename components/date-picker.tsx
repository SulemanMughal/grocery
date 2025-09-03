"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Calendar, X, ChevronDown } from "lucide-react"

interface DatePickerProps {
  value: string
  onChange: (date: string) => void
  placeholder?: string
}

export function DatePicker({ value, onChange, placeholder = "Select date" }: DatePickerProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [selectedDate, setSelectedDate] = useState<Date | null>(value ? new Date(value) : null)
  const [viewMonth, setViewMonth] = useState(new Date().getMonth())
  const [viewYear, setViewYear] = useState(new Date().getFullYear())

  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ]

  const years = Array.from({ length: 20 }, (_, i) => new Date().getFullYear() - 10 + i)

  const getDaysInMonth = (month: number, year: number) => {
    return new Date(year, month + 1, 0).getDate()
  }

  const getFirstDayOfMonth = (month: number, year: number) => {
    const firstDay = new Date(year, month, 1).getDay()
    return firstDay === 0 ? 6 : firstDay - 1 // Convert Sunday (0) to 6, Monday (1) to 0, etc.
  }

  const formatDisplayDate = (date: Date | null) => {
    if (!date) return placeholder
    return date.toLocaleDateString("en-GB") // DD/MM/YYYY format
  }

  const handleDateSelect = (day: number) => {
    const newDate = new Date(viewYear, viewMonth, day)
    setSelectedDate(newDate)
  }

  const handleConfirm = () => {
    if (selectedDate) {
      onChange(selectedDate.toISOString().split("T")[0])
      setIsOpen(false)
    }
  }

  const handleCancel = () => {
    setSelectedDate(value ? new Date(value) : null)
    setIsOpen(false)
  }

  const renderCalendarDays = () => {
    const daysInMonth = getDaysInMonth(viewMonth, viewYear)
    const firstDay = getFirstDayOfMonth(viewMonth, viewYear)
    const days = []

    // Previous month's trailing days
    const prevMonth = viewMonth === 0 ? 11 : viewMonth - 1
    const prevYear = viewMonth === 0 ? viewYear - 1 : viewYear
    const daysInPrevMonth = getDaysInMonth(prevMonth, prevYear)

    for (let i = firstDay - 1; i >= 0; i--) {
      days.push(
        <button
          key={`prev-${daysInPrevMonth - i}`}
          className="h-10 w-10 text-gray-400 hover:bg-gray-50 rounded-md text-sm font-medium"
          onClick={() => {
            setViewMonth(prevMonth)
            setViewYear(prevYear)
            handleDateSelect(daysInPrevMonth - i)
          }}
        >
          {daysInPrevMonth - i}
        </button>,
      )
    }

    // Current month days
    for (let day = 1; day <= daysInMonth; day++) {
      const isSelected =
        selectedDate &&
        selectedDate.getDate() === day &&
        selectedDate.getMonth() === viewMonth &&
        selectedDate.getFullYear() === viewYear

      days.push(
        <button
          key={day}
          className={`h-10 w-10 rounded-md text-sm font-medium transition-colors ${
            isSelected ? "bg-[#7b1aff] text-white hover:bg-[#6914d9]" : "text-gray-900 hover:bg-gray-50"
          }`}
          onClick={() => handleDateSelect(day)}
        >
          {day}
        </button>,
      )
    }

    // Next month's leading days
    const remainingCells = 42 - days.length
    const nextMonth = viewMonth === 11 ? 0 : viewMonth + 1
    const nextYear = viewMonth === 11 ? viewYear + 1 : viewYear

    for (let day = 1; day <= remainingCells; day++) {
      days.push(
        <button
          key={`next-${day}`}
          className="h-10 w-10 text-gray-400 hover:bg-gray-50 rounded-md text-sm font-medium"
          onClick={() => {
            setViewMonth(nextMonth)
            setViewYear(nextYear)
            handleDateSelect(day)
          }}
        >
          {day}
        </button>,
      )
    }

    return days
  }

  return (
    <>
      <div
        className="flex items-center justify-between border border-gray-300 rounded-md px-3 py-2.5 cursor-pointer hover:border-gray-400 bg-white h-12"
        onClick={() => setIsOpen(true)}
      >
        <span className="text-sm text-gray-900">{formatDisplayDate(selectedDate)}</span>
        <Calendar className="h-4 w-4 text-gray-500" />
      </div>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="max-w-sm p-0 gap-0" showCloseButton={false} >
          <DialogHeader className="flex flex-row items-center justify-between p-6 pb-4 space-y-0">
            <DialogTitle className="text-lg font-semibold text-gray-900">Finalize start date</DialogTitle>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleCancel}
              className="h-8 w-8 p-0 rounded-full hover:bg-gray-100 border border-gray-300 hover:cursor-pointer"
            >
              <X className="h-4 w-4 text-gray-500" />
            </Button>
          </DialogHeader>

          <div className="px-6 pb-6 space-y-6">
            <div className="flex gap-3">
              <Select value={months[viewMonth]} onValueChange={(month) => setViewMonth(months.indexOf(month))}>
                <SelectTrigger className="flex-1 h-10 border-gray-300">
                  <SelectValue />
                  {/* <ChevronDown className="h-4 w-4 text-gray-500" /> */}
                </SelectTrigger>
                <SelectContent>
                  {months.map((month) => (
                    <SelectItem key={month} value={month}>
                      {month}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Select value={viewYear.toString()} onValueChange={(year) => setViewYear(Number.parseInt(year))}>
                <SelectTrigger className="w-30 h-10 border-gray-300">
                  <SelectValue />
                  {/* <ChevronDown className="h-4 w-4 text-gray-500" /> */}
                </SelectTrigger>
                <SelectContent>
                  {years.map((year) => (
                    <SelectItem key={year} value={year.toString()}>
                      {year}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-3">
              <div className="grid grid-cols-7 gap-1 text-center">
                {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((day) => (
                  <div key={day} className="h-10 flex items-center justify-center text-sm font-medium text-gray-500">
                    {day}
                  </div>
                ))}
              </div>

              <div className="grid grid-cols-7 gap-1 ">{renderCalendarDays()}</div>
            </div>

            <div className="flex gap-3 pt-2">
              <Button
                variant="outline"
                onClick={handleCancel}
                className="flex-1 h-12 bg-[#efeffd] border-[#efeffd] text-[#7b1aff] hover:bg-[#e5e5fb] hover:border-[#e5e5fb] font-medium"
              >
                Cancel
              </Button>
              <Button
                onClick={handleConfirm}
                className="flex-1 h-12 bg-[#7b1aff] hover:bg-[#6914d9] text-white font-medium"
                disabled={!selectedDate}
              >
                Select
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  )
}
