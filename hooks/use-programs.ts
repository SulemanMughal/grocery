"use client"

import { useState } from "react"
import type { Program, SortField, SortDirection } from "@/types/program"

const initialPrograms: Program[] = [
  {
    id: "1",
    name: "Web AI Pentest - B2 team",
    startDate: "Nov02, 2023",
    assetIdentifier: "Trustline.sa",
    description: "Complete Form",
    bountyEligibility: "ELIGIBLE",
  },
  {
    id: "2",
    name: "Web AI Pentest - B2 team",
    startDate: "Nov02, 2023",
    assetIdentifier: "Trustline.sa",
    description: "Under Review",
    bountyEligibility: "INELIGIBLE",
  },
  {
    id: "3",
    name: "Web AI Pentest - B2 team",
    startDate: "Nov02, 2023",
    assetIdentifier: "Trustline.sa",
    description: "5 open Findings",
    bountyEligibility: "ELIGIBLE",
  },
  {
    id: "4",
    name: "Web AI Pentest - B2 team",
    startDate: "Nov02, 2023",
    assetIdentifier: "Trustline.sa",
    description: "74 Resolved Reports",
    bountyEligibility: "INELIGIBLE",
  },
  {
    id: "5",
    name: "Web AI Pentest - B2 team",
    startDate: "Nov02, 2023",
    assetIdentifier: "Trustline.sa",
    description: "71 Resolved Reports",
    bountyEligibility: "ELIGIBLE",
  },
  {
    id: "6",
    name: "Web AI Pentest - B2 team",
    startDate: "Nov02, 2023",
    assetIdentifier: "Trustline.sa",
    description: "71 Resolved Reports",
    bountyEligibility: "INELIGIBLE",
  },
]

export function usePrograms() {
  const [programs, setPrograms] = useState<Program[]>(initialPrograms)
  const [sortField, setSortField] = useState<SortField | null>(null)
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc")

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc")
    } else {
      setSortField(field)
      setSortDirection("asc")
    }
  }

  const sortedPrograms = [...programs].sort((a, b) => {
    if (!sortField) return 0

    let aValue = a[sortField]
    let bValue = b[sortField]

    if (sortDirection === "desc") {
      ;[aValue, bValue] = [bValue, aValue]
    }

    return aValue.localeCompare(bValue)
  })

  const addProgram = (program: Program) => {
    setPrograms([program, ...programs])
  }

  const deleteProgram = (programId: string) => {
    setPrograms(programs.filter((p) => p.id !== programId))
  }

  const editProgram = (programId: string) => {
    console.log("Edit program:", programId)
  }

  const viewProgram = (programId: string) => {
    console.log("View program:", programId)
  }

  return {
    programs: sortedPrograms,
    sortField,
    sortDirection,
    handleSort,
    addProgram,
    deleteProgram,
    editProgram,
    viewProgram,
  }
}
