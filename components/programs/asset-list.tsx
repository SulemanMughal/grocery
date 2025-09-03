"use client"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Smartphone, Globe, Trash2 } from "lucide-react"
import type { Asset } from "@/types/program"

interface AssetListProps {
  assets: Asset[]
  onRemoveAsset: (id: string) => void
}

export function AssetList({ assets, onRemoveAsset }: AssetListProps) {
  if (assets.length === 0) return null

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-5 gap-4 text-sm font-medium text-gray-700 border-b pb-2">
        <div>Type</div>
        <div>Asset Identifier</div>
        <div>Description</div>
        <div>Bounty</div>
        <div></div>
      </div>

      {assets.map((asset) => (
        <div key={asset.id} className="grid grid-cols-5 gap-4 items-center py-3 border-b border-gray-100">
          <div className="flex items-center gap-2">
            {asset.type === "MOBILE" ? (
              <div className="w-6 h-6 bg-gray-800 rounded flex items-center justify-center">
                <Smartphone className="w-3 h-3 text-white" />
              </div>
            ) : (
              <div className="w-6 h-6 bg-gray-600 rounded flex items-center justify-center">
                <Globe className="w-3 h-3 text-white" />
              </div>
            )}
          </div>
          <div className="text-[#7b1aff] text-sm">{asset.identifier}</div>
          <div className="text-gray-600 text-sm">{asset.description}</div>
          <div>
            <Badge
              variant={asset.bountyEligibility === "ELIGIBLE" ? "default" : "destructive"}
              className={
                asset.bountyEligibility === "ELIGIBLE"
                  ? "bg-green-100 text-green-700 hover:bg-green-100"
                  : "bg-red-100 text-red-700 hover:bg-red-100"
              }
            >
              {asset.bountyEligibility === "ELIGIBLE" ? "Eligible" : "Ineligible"}
            </Badge>
          </div>
          <div>
            <Button
              onClick={() => onRemoveAsset(asset.id)}
              variant="ghost"
              size="sm"
              className="h-8 w-8 p-0 hover:bg-red-50"
            >
              <Trash2 className="h-4 w-4 text-gray-400 hover:text-red-500" />
            </Button>
          </div>
        </div>
      ))}
    </div>
  )
}
