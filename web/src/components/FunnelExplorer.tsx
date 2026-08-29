import { useRef, useState, type KeyboardEvent } from "react";
import Plot from "react-plotly.js";

import {
  INITIAL_EXPLORER_STATE,
  LABEL_MODES,
  formatStageValue,
  type FunnelData,
  type FunnelKey,
  type LabelMode,
} from "../lib/funnel-data";

interface Props {
  data: FunnelData;
}

const FUNNEL_KEYS: FunnelKey[] = ["user", "ride"];
const STAGE_COLORS = ["#4f7465", "#426c5c", "#365f51", "#2a5145"];

export default function FunnelExplorer({ data }: Props) {
  const [activeFunnel, setActiveFunnel] = useState<FunnelKey>(
    INITIAL_EXPLORER_STATE.funnel,
  );
  const [labelMode, setLabelMode] = useState<LabelMode>(
    INITIAL_EXPLORER_STATE.mode,
  );
  const tabRefs = useRef<Record<FunnelKey, HTMLButtonElement | null>>({
    user: null,
    ride: null,
  });
  const modeRefs = useRef<Record<LabelMode, HTMLInputElement | null>>({
    absolute: null,
    percentTop: null,
    percentPrevious: null,
  });

  const funnel = data.funnels[activeFunnel];
  const selectedModeLabel = LABEL_MODES.find(
    (mode) => mode.value === labelMode,
  )?.label;
  const resetDisabled =
    activeFunnel === INITIAL_EXPLORER_STATE.funnel &&
    labelMode === INITIAL_EXPLORER_STATE.mode;

  function selectFunnel(nextFunnel: FunnelKey) {
    setActiveFunnel(nextFunnel);
    tabRefs.current[nextFunnel]?.focus();
  }

  function handleTabKeyDown(event: KeyboardEvent<HTMLButtonElement>) {
    const currentIndex = FUNNEL_KEYS.indexOf(activeFunnel);
    let nextIndex: number | null = null;
    if (event.key === "ArrowRight") nextIndex = (currentIndex + 1) % FUNNEL_KEYS.length;
    if (event.key === "ArrowLeft") {
      nextIndex = (currentIndex - 1 + FUNNEL_KEYS.length) % FUNNEL_KEYS.length;
    }
    if (event.key === "Home") nextIndex = 0;
    if (event.key === "End") nextIndex = FUNNEL_KEYS.length - 1;
    if (nextIndex !== null) {
      event.preventDefault();
      selectFunnel(FUNNEL_KEYS[nextIndex]);
    }
  }

  function selectLabelMode(nextMode: LabelMode) {
    setLabelMode(nextMode);
    modeRefs.current[nextMode]?.focus();
  }

  function handleModeKeyDown(
    event: KeyboardEvent<HTMLInputElement>,
    currentIndex: number,
  ) {
    let nextIndex: number | null = null;
    if (event.key === "ArrowRight" || event.key === "ArrowDown") {
      nextIndex = (currentIndex + 1) % LABEL_MODES.length;
    }
    if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
      nextIndex = (currentIndex - 1 + LABEL_MODES.length) % LABEL_MODES.length;
    }
    if (event.key === "Home") nextIndex = 0;
    if (event.key === "End") nextIndex = LABEL_MODES.length - 1;
    if (event.key === " " || event.key === "Enter") nextIndex = currentIndex;

    if (nextIndex !== null) {
      event.preventDefault();
      const nextMode = LABEL_MODES[nextIndex];
      if (nextMode) selectLabelMode(nextMode.value);
    }
  }

  function resetExplorer() {
    setActiveFunnel(INITIAL_EXPLORER_STATE.funnel);
    setLabelMode(INITIAL_EXPLORER_STATE.mode);
    tabRefs.current[INITIAL_EXPLORER_STATE.funnel]?.focus();
  }

  function handleResetKeyDown(event: KeyboardEvent<HTMLButtonElement>) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      resetExplorer();
    }
  }

  const visibleValues = funnel.stages.map((stage) =>
    formatStageValue(stage, labelMode),
  );
  const hoverText = funnel.stages.map(
    (stage) => {
      const percentOfTop =
        stage.percentOfTop === null ? "N/A" : `${stage.percentOfTop.toFixed(2)}%`;
      const percentOfPrevious =
        stage.percentOfPrevious === null
          ? "N/A"
          : `${stage.percentOfPrevious.toFixed(2)}%`;
      return (
        `${stage.label}<br>${stage.count.toLocaleString("en-US")} ${funnel.unit}` +
        `<br>${percentOfTop} of top` +
        `<br>${percentOfPrevious} of previous`
      );
    },
  );

  return (
    <div className="explorer-shell">
      <div className="explorer-controls">
        <div className="tabs" role="tablist" aria-label="Funnel grain">
          {FUNNEL_KEYS.map((funnelKey) => (
            <button
              key={funnelKey}
              ref={(element) => {
                tabRefs.current[funnelKey] = element;
              }}
              id={`${funnelKey}-tab`}
              type="button"
              role="tab"
              aria-selected={activeFunnel === funnelKey}
              aria-controls="funnel-panel"
              tabIndex={activeFunnel === funnelKey ? 0 : -1}
              onClick={() => selectFunnel(funnelKey)}
              onKeyDown={handleTabKeyDown}
            >
              <span>{data.funnels[funnelKey].label}</span>
              <small>{funnelKey === "user" ? "Entrant grain" : "Ride grain"}</small>
            </button>
          ))}
        </div>

        <fieldset className="mode-switcher">
          <legend>Stage labels</legend>
          <div className="mode-switcher__options">
            {LABEL_MODES.map((mode, index) => (
              <label key={mode.value}>
                <input
                  ref={(element) => {
                    modeRefs.current[mode.value] = element;
                  }}
                  type="radio"
                  name="label-mode"
                  value={mode.value}
                  checked={labelMode === mode.value}
                  onChange={() => setLabelMode(mode.value)}
                  onKeyDown={(event) => handleModeKeyDown(event, index)}
                />
                <span>{mode.label}</span>
              </label>
            ))}
          </div>
        </fieldset>

        <button
          className="reset-button"
          type="button"
          onClick={resetExplorer}
          onKeyDown={handleResetKeyDown}
          disabled={resetDisabled}
        >
          <span aria-hidden="true">↺</span> Reset
        </button>
      </div>

      <div
        id="funnel-panel"
        className="explorer-panel"
        role="tabpanel"
        aria-labelledby={`${activeFunnel}-tab`}
      >
        <div className="panel-intro">
          <div>
            <p className="panel-intro__scope">Validated full snapshot</p>
            <h3>{funnel.label}</h3>
            <p>{funnel.grain}. Counts use source data observed through the documented cutoff.</p>
          </div>
          <div className="grain-badge">
            <span>Current label</span>
            <strong>{selectedModeLabel}</strong>
          </div>
        </div>

        <p className="sr-only" aria-live="polite">
          Showing {funnel.label} with {selectedModeLabel} labels.
        </p>

        <div className="explorer-grid">
          <div className="plot-frame" aria-hidden="true">
            <Plot
              data={[
                {
                  type: "funnel",
                  orientation: "h",
                  y: funnel.stages.map((stage) => stage.label),
                  x: funnel.stages.map((stage) => stage.count),
                  text: visibleValues,
                  textinfo: "text",
                  textposition: "inside",
                  textfont: { color: "#f5f8f6", size: 14 },
                  marker: {
                    color: STAGE_COLORS,
                    line: { color: "#cfe5d9", width: 1 },
                  },
                  connector: { line: { color: "#385247", width: 1 } },
                  hovertext: hoverText,
                  hoverinfo: "text",
                },
              ]}
              layout={{
                autosize: true,
                margin: { l: 104, r: 24, t: 18, b: 18 },
                paper_bgcolor: "rgba(0,0,0,0)",
                plot_bgcolor: "rgba(0,0,0,0)",
                font: { color: "#dce7e1", family: "Inter, system-ui, sans-serif" },
                hoverlabel: {
                  bgcolor: "#14231e",
                  bordercolor: "#7f9e8e",
                  font: { color: "#f5f8f6", size: 13 },
                },
                funnelmode: "stack",
                showlegend: false,
              }}
              config={{
                displayModeBar: false,
                responsive: true,
                scrollZoom: false,
              }}
              useResizeHandler
              style={{ width: "100%", height: "100%" }}
            />
          </div>

          <div className="summary-card">
            <div className="summary-card__heading">
              <p>Accessible stage summary</p>
              <span>Exact counts remain visible in every mode</span>
            </div>
            <div className="table-wrap">
              <table>
                <caption className="sr-only">
                  {funnel.label} stage counts and conversion percentages
                </caption>
                <thead>
                  <tr>
                    <th scope="col">Stage</th>
                    <th scope="col">{selectedModeLabel}</th>
                    <th scope="col">Exact count</th>
                  </tr>
                </thead>
                <tbody>
                  {funnel.stages.map((stage) => (
                    <tr key={stage.key}>
                      <th scope="row">{stage.label}</th>
                      <td>{formatStageValue(stage, labelMode)}</td>
                      <td>{stage.count.toLocaleString("en-US")}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="summary-note">
              The first stage has no previous-stage denominator, so it appears
              as <strong>N/A</strong> in Percent of Previous mode.
            </p>
          </div>
        </div>

        <details className="method-note">
          <summary>How was this calculated?</summary>
          <p>
            The browser receives only four validated aggregate stages per funnel.
            Canonical Python <code>{data.traceability.python}</code> is reconciled
            with <code>{data.traceability.sql}</code> before the JSON artifact is replaced.
          </p>
        </details>
      </div>
    </div>
  );
}
