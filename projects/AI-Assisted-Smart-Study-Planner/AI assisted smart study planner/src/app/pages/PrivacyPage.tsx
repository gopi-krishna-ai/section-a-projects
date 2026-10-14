export function PrivacyPage() {
  const sections = [
    { title: "Information We Collect", content: "We collect information you provide directly to us, such as when you create an account (name, email address, password), add academic content (subjects, tasks, notes, events), and contact us for support.\n\nWe also automatically collect certain information when you use our service, including usage data (pages visited, features used, session duration), device information (browser type, operating system), and log data (IP address, access times)." },
    { title: "How We Use Your Information", content: "We use the information we collect to provide, maintain, and improve StudyAI services; generate personalized AI study plans based on your academic data; send you service-related communications; respond to your comments and questions; monitor and analyze usage patterns to improve our product; and detect and prevent fraudulent or abusive activity." },
    { title: "Data Storage & Security", content: "Your data is stored on secure servers with encryption at rest and in transit (TLS/SSL). We implement industry-standard security measures including regular security audits, access controls, and monitoring. While we take reasonable steps to protect your data, no method of transmission over the internet is 100% secure." },
    { title: "Data Sharing", content: "We do not sell your personal data to third parties. We may share your information with service providers who assist in operating our platform (such as cloud hosting and analytics providers), when required by law or to protect rights and safety, or in connection with a business transaction such as a merger or acquisition. All third-party providers are bound by data processing agreements." },
    { title: "Your Rights", content: "Depending on your location, you may have rights including: the right to access your personal data; the right to correct inaccurate data; the right to delete your data (right to erasure); the right to restrict processing; the right to data portability; and the right to object to processing. To exercise any of these rights, contact us at privacy@studyai.io." },
    { title: "Cookies", content: "We use essential cookies to operate our service (authentication, session management). We also use analytics cookies to understand how students use our platform. You can control cookies through your browser settings, though disabling certain cookies may affect functionality." },
    { title: "Children's Privacy", content: "StudyAI is intended for users 13 years of age and older. We do not knowingly collect personal information from children under 13. If you believe we have collected information from a child under 13, please contact us immediately." },
    { title: "Changes to This Policy", content: "We may update this Privacy Policy from time to time. We will notify you of significant changes via email or a prominent notice in our application. Your continued use of StudyAI after changes take effect constitutes acceptance of the updated policy." },
    { title: "Contact Us", content: "If you have questions about this Privacy Policy or our data practices, please contact us at:\n\nStudyAI Privacy Team\nEmail: privacy@studyai.io\nMailing address: StudyAI Inc., 123 Education Lane, San Francisco, CA 94103" },
  ];

  return (
    <div style={{ fontFamily: "Inter, sans-serif" }}>
      <section className="py-16 px-6" style={{ background: "linear-gradient(180deg, #f8fafc, #fff)" }}>
        <div className="max-w-3xl mx-auto">
          <p style={{ color: "#4F8EF7", fontWeight: 600, fontSize: "0.85rem", letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 12 }}>Legal</p>
          <h1 style={{ fontWeight: 800, fontSize: "2.5rem", color: "#0f172a", letterSpacing: "-0.02em", marginBottom: 12 }}>Privacy Policy</h1>
          <p style={{ color: "#64748b", fontSize: "0.9rem" }}>Last updated: June 22, 2026 · Effective: July 1, 2026</p>
          <p style={{ color: "#64748b", fontSize: "0.95rem", lineHeight: 1.75, marginTop: 16 }}>
            At StudyAI, we take your privacy seriously. This policy explains what data we collect, how we use it, and the choices you have. If you have questions, please <a href="mailto:privacy@studyai.io" style={{ color: "#4F8EF7" }}>contact us</a>.
          </p>
        </div>
      </section>

      <section className="pb-24 px-6">
        <div className="max-w-3xl mx-auto space-y-8">
          {sections.map(({ title, content }) => (
            <div key={title} className="p-6 rounded-2xl" style={{ background: "#fff", border: "1px solid #e2e8f0" }}>
              <h2 style={{ fontWeight: 700, fontSize: "1.1rem", color: "#0f172a", marginBottom: 12 }}>{title}</h2>
              {content.split("\n\n").map((p, i) => (
                <p key={i} style={{ color: "#64748b", fontSize: "0.9rem", lineHeight: 1.75, marginBottom: i < content.split("\n\n").length - 1 ? 12 : 0 }}>{p}</p>
              ))}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
