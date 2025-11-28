import { Button } from '@/components/livekit/button';

function GroceryIcon() {
  return (
    <svg
      width="64"
      height="64"
      viewBox="0 0 24 24"
      fill="none"
      className="text-green-600 mb-4 size-16"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M3 3H5L6.68 12.39C6.823 13.21 7.539 13.8 8.373 13.8H18.2C19.03 13.8 19.74 13.21 19.89 12.39L21 6H7"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle cx="9" cy="19" r="1.5" fill="currentColor" />
      <circle cx="17" cy="19" r="1.5" fill="currentColor" />
    </svg>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div ref={ref}>
      <section className="bg-background flex flex-col items-center justify-center text-center p-8">
        <GroceryIcon />

        <h1 className="text-foreground text-2xl font-bold mb-2">
          Welcome to FreshMart 🛒
        </h1>

        <p className="text-muted-foreground max-w-sm text-sm md:text-base leading-6 font-medium">
          Talk to your AI assistant and order groceries hands-free — just say
          what you need!
        </p>

        <Button
          variant="primary"
          size="lg"
          onClick={onStartCall}
          className="mt-6 w-64 font-semibold"
        >
          {startButtonText || 'Start Ordering Groceries'}
        </Button>
      </section>

      <div className="fixed bottom-5 left-0 flex w-full items-center justify-center">
        <p className="text-muted-foreground text-xs md:text-sm font-normal">
          Powered by LiveKit Voice AI ✨
        </p>
      </div>
    </div>
  );
};
