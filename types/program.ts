export interface Program {
  id: string
  name: string
  startDate: string
  assetIdentifier: string
  description: string
  bountyEligibility: "ELIGIBLE" | "INELIGIBLE"
}

export interface Asset {
  id: string
  type: "WEB" | "MOBILE"
  identifier: string
  description: string
  bountyEligibility: "ELIGIBLE" | "INELIGIBLE"
}

export interface NewProgramForm {
  name: string
  startDate: string
  website: string
  twitter: string
  assetType: string
  assetIdentifier: string
  description: string
  bountyEligibility: string
}

export type SortField = "name" | "startDate" | "assetIdentifier" | "description" | "bountyEligibility"
export type SortDirection = "asc" | "desc"
