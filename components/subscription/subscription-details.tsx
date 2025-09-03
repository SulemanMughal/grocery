
import { Card } from "@/components/ui/card"
import { Info } from "lucide-react"
import { CreateProgramModal } from "@/components/programs/create-program-modal"
import type { Program } from "@/types/program"


interface SubscriptionDetailsProps {
  onCreateProgram: (program: Program) => void;
}

export function SubscriptionDetails({ onCreateProgram }: SubscriptionDetailsProps) {

  return (
    <div className="space-y-4 w-full">
      <h1 className="text-xl font-medium text-gray-900">Subscription Details</h1>

      <Card className="p-4 md:p-6">
  <div className="flex flex-col gap-6 w-full md:flex-row md:items-center md:gap-0">
          {/* Subscription Info */}
          <div className="flex items-center gap-3 min-w-[220px] mb-4 md:mb-0">
            <div className="flex h-8 w-8 items-center justify-center">
              <svg width="22" height="23" viewBox="0 0 22 23" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M10.5316 20.2761C15.3786 20.2761 19.3078 16.3469 19.3078 11.4999C19.3078 6.65298 15.3786 2.72375 10.5316 2.72375C5.68466 2.72375 1.75543 6.65298 1.75543 11.4999C1.75543 16.3469 5.68466 20.2761 10.5316 20.2761Z"
                  stroke="#03BA84"
                  strokeWidth="1.31643"
                />
                <path
                  d="M10.5315 15.8882V16.7658M10.5315 15.8882C11.9857 15.8882 13.1643 14.9052 13.1643 13.6941C13.1643 12.483 11.9857 11.5001 10.5315 11.5001C9.07726 11.5001 7.89862 10.5172 7.89862 9.30604C7.89862 8.09493 9.07726 7.11199 10.5315 7.11199M10.5315 15.8882C9.07726 15.8882 7.89862 14.9052 7.89862 13.6941M10.5315 6.23438V7.11199M10.5315 7.11199C11.9857 7.11199 13.1643 8.09493 13.1643 9.30604"
                  stroke="#03BA84"
                  strokeWidth="1.31643"
                  strokeLinecap="round"
                />
              </svg>
            </div>
            <span className="font-semibold text-lg text-gray-900">Subscription 01</span>
            <span className="ml-2 text-base text-gray-500">Ends Aug 23, 2023</span>
          </div>

          {/* Divider */}
          <div className="hidden md:block mx-6 h-16 w-px bg-gray-200" />

          {/* Available */}
          <div className="flex flex-col items-start min-w-[160px] mb-4 md:mb-0">
            <span className="text-base font-semibold text-[#03BA84] flex items-center gap-1">
              Available <Info className="h-4 w-4 text-[#03BA84]" />
            </span>
            <span className="text-2xl font-bold text-[#03BA84] mt-1">8,000 SAR</span>
          </div>

          {/* Divider */}
          <div className="hidden md:block mx-6 h-16 w-px bg-gray-200" />

          {/* Consumed */}
          <div className="flex flex-col items-start min-w-[160px] mb-4 md:mb-0">
            <span className="text-base font-semibold text-gray-600 flex items-center gap-1">
              Consumed <Info className="h-4 w-4 text-gray-400" />
            </span>
            <span className="text-2xl font-bold text-gray-600 mt-1">400 SAR</span>
          </div>

          {/* Divider */}
          <div className="hidden md:block mx-6 h-16 w-px bg-gray-200" />

          {/* Total Balance */}
          <div className="flex flex-col items-start min-w-[160px] mb-4 md:mb-0">
            <span className="text-base font-semibold text-gray-900">Total Balance</span>
            <span className="text-2xl font-bold text-gray-900 mt-1">1,200 SAR</span>
          </div>

          <div className="flex-1 flex justify-end md:justify-end w-full md:w-auto">
            <div className="w-full md:w-auto">
              <CreateProgramModal onCreateProgram={onCreateProgram} />
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}
