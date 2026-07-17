type ErrorBannerProps = {
  error: string | null;
};

export function ErrorBanner({error}: ErrorBannerProps) {
  if (error === null) {
    return null;
  }

  return (
    <section className="mb-6 animate-[fadeIn_0.25s_ease-out] rounded-3xl border border-red-100 bg-red-50 p-4 text-sm font-medium text-red-700">
      {error}
    </section>
  );
}