"use client"

import { useState } from "react"
import type { Asset } from "@/types/program"

export function useAssets() {
  const [assets, setAssets] = useState<Asset[]>([])

  const addAsset = (asset: Omit<Asset, "id">) => {
    const isDuplicate = assets.some((existingAsset) => existingAsset.identifier === asset.identifier)
    if (isDuplicate) return false

    const newAsset: Asset = {
      ...asset,
      id: Date.now().toString(),
    }

    setAssets([...assets, newAsset])
    return true
  }

  const removeAsset = (id: string) => {
    setAssets(assets.filter((asset) => asset.id !== id))
  }

  const clearAssets = () => {
    setAssets([])
  }

  return {
    assets,
    addAsset,
    removeAsset,
    clearAssets,
  }
}
