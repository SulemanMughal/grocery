"use client"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { MoreVertical, ChevronDown } from "lucide-react"
import type { Program, SortField, SortDirection } from "@/types/program"

interface ProgramsTableProps {
  programs: Program[]
  sortField: SortField | null
  sortDirection: SortDirection
  onSort: (field: SortField) => void
  onViewProgram: (id: string) => void
  onEditProgram: (id: string) => void
  onDeleteProgram: (id: string) => void
}

export function ProgramsTable({
  programs,
  sortField,
  sortDirection,
  onSort,
  onViewProgram,
  onEditProgram,
  onDeleteProgram,
}: ProgramsTableProps) {
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-medium text-gray-900">All programs</h2>

      <Card>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow className="border-b">
                <TableHead className="text-left font-medium text-gray-700">
                  <button
                    onClick={() => onSort("name")}
                    className="flex items-center gap-1 hover:text-gray-900 transition-colors"
                  >
                    Program
                    <ChevronDown
                      className={`h-4 w-4 transition-transform ${
                        sortField === "name" && sortDirection === "desc" ? "rotate-180" : ""
                      }`}
                    />
                  </button>
                </TableHead>
                <TableHead className="text-left font-medium text-gray-700">
                  <button
                    onClick={() => onSort("startDate")}
                    className="flex items-center gap-1 hover:text-gray-900 transition-colors"
                  >
                    Start Date
                    <ChevronDown
                      className={`h-4 w-4 transition-transform ${
                        sortField === "startDate" && sortDirection === "desc" ? "rotate-180" : ""
                      }`}
                    />
                  </button>
                </TableHead>
                <TableHead className="text-left font-medium text-gray-700">Asset Identifier</TableHead>
                <TableHead className="text-left font-medium text-gray-700">Description</TableHead>
                <TableHead className="text-left font-medium text-gray-700">Bounty Eligibility</TableHead>
                <TableHead className="w-12"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {programs.map((program) => (
                <TableRow key={program.id} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                  <TableCell className="font-medium text-[#7b1aff]">{program.name}</TableCell>
                  <TableCell className="text-gray-700">{program.startDate}</TableCell>
                  <TableCell className="text-[#7b1aff]">{program.assetIdentifier}</TableCell>
                  <TableCell className="text-gray-700">{program.description}</TableCell>
                  <TableCell>
                    <Badge
                      variant={program.bountyEligibility === "ELIGIBLE" ? "default" : "destructive"}
                      className={
                        program.bountyEligibility === "ELIGIBLE"
                          ? "bg-green-100 text-green-700 hover:bg-green-100"
                          : "bg-red-100 text-red-700 hover:bg-red-100"
                      }
                    >
                      {program.bountyEligibility === "ELIGIBLE" ? "Eligible" : "Ineligible"}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                          <MoreVertical className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => onViewProgram(program.id)}>View Details</DropdownMenuItem>
                        <DropdownMenuItem onClick={() => onEditProgram(program.id)}>Edit Program</DropdownMenuItem>
                        <DropdownMenuItem onClick={() => onDeleteProgram(program.id)} className="text-red-600">
                          Delete Program
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </Card>
    </div>
  )
}
