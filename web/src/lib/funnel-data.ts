export type LabelMode = "absolute" | "percentTop" | "percentPrevious";
export type FunnelKey = "user" | "ride";

export interface FunnelStage {
  key: string;
  label: string;
  count: number;
  percentOfTop: number | null;
  percentOfPrevious: number | null;
}

export interface FunnelDefinition {
  label: string;
  grain: string;
  unit: string;
  stages: FunnelStage[];
}

export interface FunnelData {
  schemaVersion: number;
  scope: {
    kind: "full_snapshot";
    sourceCutoff: string;
    cohortStart: null;
    cohortEndExclusive: null;
  };
  funnels: Record<FunnelKey, FunnelDefinition>;
  traceability: {
    metricContract: string;
    python: string;
    sql: string;
  };
}

export const INITIAL_EXPLORER_STATE: {
  funnel: FunnelKey;
  mode: LabelMode;
} = {
  funnel: "user",
  mode: "absolute",
};

export const LABEL_MODES: Array<{ value: LabelMode; label: string }> = [
  { value: "absolute", label: "Absolute" },
  { value: "percentTop", label: "Percent of Top" },
  { value: "percentPrevious", label: "Percent of Previous" },
];

export function formatStageValue(stage: FunnelStage, mode: LabelMode): string {
  if (mode === "absolute") {
    return stage.count.toLocaleString("en-US");
  }

  const value =
    mode === "percentTop" ? stage.percentOfTop : stage.percentOfPrevious;
  return value === null ? "N/A" : `${value.toFixed(2)}%`;
}
