interface ProgressBarProps {
  steps: string[];
  /** Zero-based index of current step */
  currentStep: number;
}

// export this part
export default function ProgressBar({
  steps,
  currentStep,
}: ProgressBarProps) {
  const safeCurrentStep = Math.min(
    Math.max(currentStep, 0),
    steps.length - 1
  );

  return (
    <div
      className="flex flex-col space-y-3"
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={steps.length - 1}
      aria-valuenow={safeCurrentStep}
    >
      {steps.map((step, idx) => {
        const isCompleted = idx < safeCurrentStep;
        const isCurrent = idx === safeCurrentStep;

        return (
          <div
            key={step}
            className="flex items-center space-x-3"
            aria-current={isCurrent ? "step" : undefined}
          >
            {/* Indicator */}
            <div
              className={`
                w-3.5 h-3.5 rounded-full transition-colors
                ${isCompleted || isCurrent ? "bg-brand" : "bg-border"}
                ${isCurrent ? "ring-2 ring-brand/40" : ""}
              `}
            />

            {/* Label */}
            <span
              className={`
                text-sm transition-colors
                ${isCompleted ? "text-text-primary" : ""}
                ${isCurrent ? "text-text-primary font-medium" : ""}
                ${!isCompleted && !isCurrent ? "text-text-muted" : ""}
              `}
            >
              {step}
            </span>
          </div>
        );
      })}
    </div>
  );
}
