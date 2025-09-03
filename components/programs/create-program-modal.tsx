"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { DatePicker } from "@/components/date-picker"
import { AssetList } from "./asset-list"
import { useAssets } from "@/hooks/use-assets"
import type { Program, NewProgramForm } from "@/types/program"


interface CreateProgramModalProps {
  onCreateProgram: (program: Program) => void
}

export function CreateProgramModal({ onCreateProgram }: CreateProgramModalProps) {

  const [isOpen, setIsOpen] = useState(false)
  const { assets, addAsset, removeAsset, clearAssets } = useAssets()
  const [formData, setFormData] = useState<NewProgramForm>({
    name: "",
    startDate: "",
    website: "",
    twitter: "",
    assetType: "",
    assetIdentifier: "",
    description: "",
    bountyEligibility: "",
  })
  const [websiteError, setWebsiteError] = useState<string>("");

  const handleAddAsset = () => {
    if (!formData.assetIdentifier.trim() || !formData.assetType || !formData.bountyEligibility) return

    const success = addAsset({
      type: formData.assetType as "WEB" | "MOBILE",
      identifier: formData.assetIdentifier,
      description: formData.description,
      bountyEligibility: formData.bountyEligibility as "ELIGIBLE" | "INELIGIBLE",
    })

    if (success) {
      setFormData({
        ...formData,
        assetType: "",
        assetIdentifier: "",
        description: "",
        bountyEligibility: "",
      })
    }
  }

  const validateWebsite = (url: string) => {
    if (!url) return "";
    try {
      new URL(url);
      return "";
    } catch {
      return "Please enter a valid website URL.";
    }
  };

  const handleWebsiteChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setFormData({ ...formData, website: value });
    setWebsiteError(validateWebsite(value));
  };

  const handleSubmit = () => {
    const websiteValidation = validateWebsite(formData.website);
    setWebsiteError(websiteValidation);
    if (!formData.name.trim() || !formData.startDate || assets.length === 0 || websiteValidation) return;

    const firstAsset = assets[0];
    const program: Program = {
      id: Date.now().toString(),
      name: formData.name,
      startDate: formData.startDate,
      assetIdentifier: firstAsset.identifier,
      description: firstAsset.description,
      bountyEligibility: firstAsset.bountyEligibility,
    };

    onCreateProgram(program);

    setFormData({
      name: "",
      startDate: "",
      website: "",
      twitter: "",
      assetType: "",
      assetIdentifier: "",
      description: "",
      bountyEligibility: "",
    });
    setWebsiteError("");
    clearAssets();
    setIsOpen(false);
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
  <Button className="text-[#7b1aff] hover:bg-[#EFEFFD] hover:cursor-pointer bg-[#EFEFFD] whitespace-nowrap w-full md:w-auto">Create Program</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-3xl  max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
          <DialogTitle className="text-xl font-semibold">Create Program</DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="program-name" className="text-sm font-medium">
                Program Name <span className="text-red-500">*</span>
              </Label>
              <Input
                id="program-name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="h-12"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="start-date" className="text-sm font-medium">
                Start Date <span className="text-red-500">*</span>
              </Label>
              <DatePicker
                value={formData.startDate}
                onChange={(date) => setFormData({ ...formData, startDate: date })}
                placeholder="Select start date"
                
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="website" className="text-sm font-medium">
                Website
              </Label>
              <Input
                id="website"
                value={formData.website}
                onChange={handleWebsiteChange}
                placeholder="Enter Your Website"
                className="h-12"
                type="url"
                aria-invalid={!!websiteError}
              />
              {websiteError && (
                <span className="text-xs text-red-500">{websiteError}</span>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="twitter" className="text-sm font-medium">
                Twitter / X
              </Label>
              <Input
                id="twitter"
                value={formData.twitter}
                onChange={(e) => setFormData({ ...formData, twitter: e.target.value })}
                placeholder="Enter @Username"
                className="h-12"
              />
            </div>
          </div>
            

            
          <div className="space-y-4 ">
            <div className="space-y-2">
              <Label className="text-sm font-medium">Asset You Want to Test</Label>
              <Select
                value={formData.assetType}
                onValueChange={(value) => setFormData({ ...formData, assetType: value })}
              >
                <SelectTrigger className="h-12 w-full">
                  <SelectValue placeholder="Please Select" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="WEB">WEB</SelectItem>
                  <SelectItem value="MOBILE">MOBILE</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="asset-identifier" className="text-sm font-medium">
                Asset Identifier
              </Label>
              <Input
                id="asset-identifier"
                value={formData.assetIdentifier}
                onChange={(e) => setFormData({ ...formData, assetIdentifier: e.target.value })}
                placeholder="Write your asset Identifier"
                className="h-12"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="description" className="text-sm font-medium">
                Description
              </Label>
              <Textarea
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Description"
                className="min-h-[80px] resize-none"
              />
            </div>

            <div className="space-y-2">
              <Label className="text-sm font-medium">Bounty Eligibility</Label>
            </div>
            <div className="flex items-center gap-4 justify-between">
              <div className="flex-1 space-y-2">
                
                <Select
                  value={formData.bountyEligibility}
                  onValueChange={(value) => setFormData({ ...formData, bountyEligibility: value })}
                  
                >
                  <SelectTrigger className="h-12 w-full">
                    <SelectValue placeholder="Please Select" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ELIGIBLE">Eligible</SelectItem>
                    <SelectItem value="INELIGIBLE">Ineligible</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button onClick={handleAddAsset} className="bg-[#7b1aff] hover:bg-[#6914d9] text-white px-8">
                Add
              </Button>
            </div>
          </div>

          <AssetList assets={assets} onRemoveAsset={removeAsset} />

          <div className="flex gap-3 pt-4">
            <Button
              onClick={() => setIsOpen(false)}
              variant="outline"
              className="flex-1 h-12 bg-[#efeffd] text-[#7b1aff] border-[#efeffd] hover:bg-[#e5e5fb]"
            >
              Cancel
            </Button>
            <Button onClick={handleSubmit} className="flex-1 h-12 bg-[#7b1aff] hover:bg-[#6914d9] text-white">
              Submit
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
