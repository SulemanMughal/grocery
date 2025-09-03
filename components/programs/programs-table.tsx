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
                          ? "bg-transparent text-green-700 hover:bg-transparent"
                          : "bg-transparent text-red-700 hover:bg-transparent"
                      }
                    >
                      <div className="flex items-center gap-1">
                        {program.bountyEligibility === "ELIGIBLE" ? (
                          <svg width="14" height="15" viewBox="0 0 14 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12.2156 5.27693C12.554 5.61118 12.6998 6.03234 12.7681 6.53226C12.8334 7.01409 12.8334 7.62659 12.8334 8.38609V8.44734C12.8334 9.20684 12.8334 9.81934 12.7681 10.3012C12.6998 10.8011 12.554 11.2223 12.2156 11.5565C11.8773 11.8908 11.4515 12.0348 10.9451 12.1019C10.4581 12.1667 9.83797 12.1667 9.06914 12.1667H6.19622C5.42739 12.1667 4.80789 12.1667 4.32022 12.1019C3.81389 12.0348 3.38806 11.8908 3.04972 11.5565C2.85275 11.36 2.70572 11.1192 2.62097 10.8542C3.12905 10.9166 3.75847 10.9166 4.48472 10.9166H7.40722C8.15447 10.9166 8.79847 10.9166 9.31472 10.8483C9.86714 10.7748 10.3974 10.6092 10.8273 10.1845C11.2566 9.75984 11.4246 9.23601 11.4987 8.69001C11.5687 8.18018 11.5687 7.54376 11.5681 6.80468V6.69501C11.5681 5.97751 11.5681 5.35568 11.504 4.85284C11.7723 4.94093 12.0103 5.07393 12.2156 5.27693ZM5.94597 5.77801C5.4023 5.77801 4.96189 6.21318 4.96189 6.74984C4.96189 7.28651 5.4023 7.72226 5.94597 7.72226C6.48905 7.72226 6.92947 7.28709 6.92947 6.74984C6.92947 6.21318 6.48905 5.77801 5.94597 5.77801Z" fill="#1CC190"/>
                            <path fillRule="evenodd" clipRule="evenodd" d="M1.66071 3.90494C1.16663 4.39319 1.16663 5.17835 1.16663 6.74985C1.16663 8.32135 1.16663 9.1071 1.66071 9.59535C2.15479 10.0836 2.94988 10.0836 4.54004 10.0836H7.35171C8.94129 10.0836 9.73638 10.0836 10.2305 9.59535C10.7245 9.1071 10.7245 8.32135 10.7245 6.74985C10.7245 5.17894 10.7245 4.39319 10.2305 3.90494C9.73638 3.41669 8.94129 3.41669 7.35113 3.41669H4.54004C2.94988 3.41669 2.15421 3.41669 1.66071 3.90494ZM4.11829 6.74985C4.11829 5.75235 4.93671 4.94444 5.94588 4.94444C6.95504 4.94444 7.77288 5.75294 7.77288 6.74985C7.77288 7.74735 6.95504 8.55585 5.94588 8.55585C4.93671 8.55585 4.11829 7.74735 4.11829 6.74985ZM9.03813 8.27819C8.80479 8.27819 8.61638 8.09152 8.61638 7.8611V5.63919C8.61638 5.40935 8.80479 5.22269 9.03813 5.22269C9.14932 5.22222 9.25615 5.26587 9.33521 5.34405C9.41427 5.42224 9.4591 5.52858 9.45988 5.63977V7.86227C9.45895 7.9733 9.41403 8.07944 9.33497 8.15741C9.25591 8.23537 9.14916 8.27881 9.03813 8.27819ZM2.43188 7.8611C2.43188 8.09152 2.62029 8.2776 2.85363 8.2776C3.08638 8.2776 3.27479 8.09094 3.27479 7.8611V5.63919C3.27402 5.52815 3.22925 5.42196 3.1503 5.34388C3.07135 5.2658 2.96466 5.22222 2.85363 5.22269C2.62029 5.22269 2.43188 5.40935 2.43188 5.63977V7.8611Z" fill="#1CC190"/>
                          </svg>
                        ) : (
                          <svg width="14" height="15" viewBox="0 0 14 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12.2156 5.27693C12.554 5.61118 12.6998 6.03234 12.7681 6.53226C12.8334 7.01409 12.8334 7.62659 12.8334 8.38609V8.44734C12.8334 9.20684 12.8334 9.81934 12.7681 10.3012C12.6998 10.8011 12.554 11.2223 12.2156 11.5565C11.8773 11.8908 11.4515 12.0348 10.9451 12.1019C10.4581 12.1667 9.83797 12.1667 9.06914 12.1667H6.19622C5.42739 12.1667 4.80789 12.1667 4.32022 12.1019C3.81389 12.0348 3.38806 11.8908 3.04972 11.5565C2.85275 11.36 2.70572 11.1192 2.62097 10.8542C3.12905 10.9166 3.75847 10.9166 4.48472 10.9166H7.40722C8.15447 10.9166 8.79847 10.9166 9.31472 10.8483C9.86714 10.7748 10.3974 10.6092 10.8273 10.1845C11.2566 9.75984 11.4246 9.23601 11.4987 8.69001C11.5687 8.18018 11.5687 7.54376 11.5681 6.80468V6.69501C11.5681 5.97751 11.5681 5.35568 11.504 4.85284C11.7723 4.94093 12.0103 5.07393 12.2156 5.27693ZM5.94597 5.77801C5.4023 5.77801 4.96189 6.21318 4.96189 6.74984C4.96189 7.28651 5.4023 7.72226 5.94597 7.72226C6.48905 7.72226 6.92947 7.28709 6.92947 6.74984C6.92947 6.21318 6.48905 5.77801 5.94597 5.77801Z" fill="#dc2626"/>
                            <path fillRule="evenodd" clipRule="evenodd" d="M1.66071 3.90494C1.16663 4.39319 1.16663 5.17835 1.16663 6.74985C1.16663 8.32135 1.16663 9.1071 1.66071 9.59535C2.15479 10.0836 2.94988 10.0836 4.54004 10.0836H7.35171C8.94129 10.0836 9.73638 10.0836 10.2305 9.59535C10.7245 9.1071 10.7245 8.32135 10.7245 6.74985C10.7245 5.17894 10.7245 4.39319 10.2305 3.90494C9.73638 3.41669 8.94129 3.41669 7.35113 3.41669H4.54004C2.94988 3.41669 2.15421 3.41669 1.66071 3.90494ZM4.11829 6.74985C4.11829 5.75235 4.93671 4.94444 5.94588 4.94444C6.95504 4.94444 7.77288 5.75294 7.77288 6.74985C7.77288 7.74735 6.95504 8.55585 5.94588 8.55585C4.93671 8.55585 4.11829 7.74735 4.11829 6.74985ZM9.03813 8.27819C8.80479 8.27819 8.61638 8.09152 8.61638 7.8611V5.63919C8.61638 5.40935 8.80479 5.22269 9.03813 5.22269C9.14932 5.22222 9.25615 5.26587 9.33521 5.34405C9.41427 5.42224 9.4591 5.52858 9.45988 5.63977V7.86227C9.45895 7.9733 9.41403 8.07944 9.33497 8.15741C9.25591 8.23537 9.14916 8.27881 9.03813 8.27819ZM2.43188 7.8611C2.43188 8.09152 2.62029 8.2776 2.85363 8.2776C3.08638 8.2776 3.27479 8.09094 3.27479 7.8611V5.63919C3.27402 5.52815 3.22925 5.42196 3.1503 5.34388C3.07135 5.2658 2.96466 5.22222 2.85363 5.22269C2.62029 5.22269 2.43188 5.40935 2.43188 5.63977V7.8611Z" fill="#dc2626"/>
                          </svg>
                        )}
                        {program.bountyEligibility === "ELIGIBLE" ? "Eligible" : "Ineligible"}
                      </div>
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
