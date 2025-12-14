interface CircularProgressProps {
  progress: number; // 0 to 100
  label: string;
}

export default function CircularProgress({ progress, label }: CircularProgressProps) {
  const radius = 40;
  const stroke = 6;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <div className="flex flex-col items-center space-y-2">
      <svg height={radius * 2} width={radius * 2}>
        <circle
          stroke="#35371fff"
          fill="transparent"
          strokeWidth={stroke}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <circle
          stroke="#68f163ff"
          fill="transparent"
          strokeWidth={stroke}
          strokeLinecap="round"
          r={normalizedRadius}
          cx={radius}
          cy={radius}
          strokeDasharray={circumference + " " + circumference}
          strokeDashoffset={strokeDashoffset}
          style={{ transition: "stroke-dashoffset 2s ease" }}
        />
      </svg>
      <span className="text-sm text-text-primary">{label}</span>
    </div>
  );
}
