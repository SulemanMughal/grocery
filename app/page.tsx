"use client"

import { SubscriptionDetails } from "@/components/subscription/subscription-details"
import { ProgramsTable } from "@/components/programs/programs-table"
import { usePrograms } from "@/hooks/use-programs"

export default function ProgramsPage() {
  const { programs, sortField, sortDirection, handleSort, addProgram, deleteProgram, editProgram, viewProgram } =
    usePrograms()

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-6 lg:p-8">
      <div className="mx-auto max-w-7xl space-y-6">
        {/* Header */}
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <h1 className="text-2xl font-semibold text-gray-900">Programs</h1>
        </div>
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          
          <SubscriptionDetails onCreateProgram={addProgram} />
          
        </div>

        <ProgramsTable
          programs={programs}
          sortField={sortField}
          sortDirection={sortDirection}
          onSort={handleSort}
          onViewProgram={viewProgram}
          onEditProgram={editProgram}
          onDeleteProgram={deleteProgram}
        />
      </div>
    </div>
  )
}
