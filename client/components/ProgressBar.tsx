interface ProgressBarProps {
  steps: string[];
  currentStep: number;
}

export default function ProgressBar({ steps, currentStep }: ProgressBarProps) {
  return (
    <div className="flex flex-col space-y-2">
      {steps.map((step, idx) => (
        <div key={step} className="flex items-center space-x-2">
          <div
            className={`w-3 h-3 rounded-full ${
              idx <= currentStep ? "bg-brand" : "bg-border"
            }`}
          />
          <span className={idx <= currentStep ? "text-text-primary" : "text-text-muted"}>
            {step}
          </span>
        </div>
      ))}
    </div>
  );
}
