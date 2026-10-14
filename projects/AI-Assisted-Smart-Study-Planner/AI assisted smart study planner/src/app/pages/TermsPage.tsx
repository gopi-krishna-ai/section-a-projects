export function TermsPage() {
  const sections = [
    { title: "Acceptance of Terms", content: "By creating a StudyAI account or using our services, you agree to be bound by these Terms of Service and our Privacy Policy. If you don't agree, please don't use our services. We may update these terms periodically and will notify you of material changes." },
    { title: "Description of Service", content: "StudyAI provides an AI-powered study planning platform for students, including features such as AI study plan generation, task tracking, calendar management, Pomodoro timers, note-taking, and analytics. We reserve the right to modify or discontinue any feature with reasonable notice." },
    { title: "User Accounts", content: "You must be at least 13 years old to use StudyAI. You are responsible for maintaining the security of your account credentials and for all activity that occurs under your account. You must provide accurate information when creating your account. You may not share your account with others or create multiple accounts for deceptive purposes." },
    { title: "Acceptable Use", content: "You agree not to: use StudyAI for any unlawful purpose; attempt to gain unauthorized access to any part of the service; scrape, copy, or redistribute our content without permission; upload malicious code or interfere with our systems; impersonate other users or StudyAI staff; or violate any applicable laws or regulations." },
    { title: "Intellectual Property", content: "StudyAI and its original content, features, and functionality are and will remain the exclusive property of StudyAI Inc. Our trademarks and trade dress may not be used in connection with any product or service without prior written consent. Your content remains your property, but you grant us a license to use it to provide our services." },
    { title: "Paid Plans & Billing", content: "Paid plans are billed on a monthly or annual basis. You authorize us to charge your payment method on a recurring basis. Refunds are available within 7 days of a charge if you haven't significantly used the Pro features. We reserve the right to change pricing with 30 days notice. Taxes may apply based on your location." },
    { title: "Termination", content: "You may terminate your account at any time from Settings → Account. We reserve the right to suspend or terminate accounts that violate these terms, with or without notice for egregious violations. Upon termination, your right to use StudyAI ceases. We may retain certain data as required by law." },
    { title: "Disclaimers", content: "StudyAI is provided 'as is' without warranties of any kind, expressed or implied. We do not guarantee that our AI predictions will be accurate or that our service will meet your specific academic goals. Results vary by individual. We are not liable for any academic outcomes." },
    { title: "Limitation of Liability", content: "To the maximum extent permitted by law, StudyAI shall not be liable for any indirect, incidental, special, or consequential damages arising from your use of the service. Our total liability shall not exceed the amount you paid us in the 12 months preceding the claim." },
    { title: "Contact", content: "For questions about these Terms, contact us at legal@studyai.io or write to:\n\nStudyAI Inc.\n123 Education Lane\nSan Francisco, CA 94103" },
  ];

  return (
    <div style={{ fontFamily: "Inter, sans-serif" }}>
      <section className="py-16 px-6" style={{ background: "linear-gradient(180deg, #f8fafc, #fff)" }}>
        <div className="max-w-3xl mx-auto">
          <p style={{ color: "#4F8EF7", fontWeight: 600, fontSize: "0.85rem", letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 12 }}>Legal</p>
          <h1 style={{ fontWeight: 800, fontSize: "2.5rem", color: "#0f172a", letterSpacing: "-0.02em", marginBottom: 12 }}>Terms of Service</h1>
          <p style={{ color: "#64748b", fontSize: "0.9rem" }}>Last updated: June 22, 2026 · Effective: July 1, 2026</p>
          <p style={{ color: "#64748b", fontSize: "0.95rem", lineHeight: 1.75, marginTop: 16 }}>
            Please read these Terms of Service carefully before using StudyAI. By using our service, you agree to these terms.
          </p>
        </div>
      </section>

      <section className="pb-24 px-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {sections.map(({ title, content }) => (
            <div key={title} className="p-6 rounded-2xl" style={{ background: "#fff", border: "1px solid #e2e8f0" }}>
              <h2 style={{ fontWeight: 700, fontSize: "1.05rem", color: "#0f172a", marginBottom: 10 }}>{title}</h2>
              {content.split("\n\n").map((p, i) => (
                <p key={i} style={{ color: "#64748b", fontSize: "0.875rem", lineHeight: 1.75, marginBottom: i < content.split("\n\n").length - 1 ? 10 : 0 }}>{p}</p>
              ))}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
