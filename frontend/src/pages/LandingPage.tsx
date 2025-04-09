import React from "react";
import { useNavigate } from "react-router-dom";

export default function LandingPage() {
  const navigate = useNavigate();


  return (
    <div className="min-h-screen bg-white text-gray-800">
      <header className="relative bg-gradient-to-r from-indigo-500 to-purple-600 text-white py-20 px-4 text-center">
        {/* Logo and Company Name */}
      <div className="absolute top-4 left-4 flex items-center space-x-4">
        <img
          src={require("../assets/images/tralpinechat_small.png")} // Replace with the path to your logo
          alt="Company Logo"
          className="h-12 w-auto" // Adjust size as needed
        />
        <span className="text-2xl font-bold">Tralpine</span>
      </div>
        {/* LOGIN BUTTON */}
        <div className="absolute top-4 right-4">
          <button onClick={() => navigate("/login")} className="px-4 py-2 bg-white text-indigo-600 font-semibold rounded-xl shadow hover:shadow-md transition">
            Login
          </button>
        </div>
        <h1 className="text-4xl md:text-6xl font-bold mb-4">
          AI-Powered Troubleshooting Assistant — Free for Early Adopters
        </h1>
        <p className="text-lg md:text-xl max-w-2xl mx-auto">
          Create a smart, step-by-step support experience for your customers — with zero code and no upfront cost.
        </p>
        <button onClick={() => navigate("/register")} className="mt-8 px-6 py-3 bg-white text-indigo-600 font-semibold rounded-2xl shadow-md hover:shadow-xl transition">
          Get My Free Assistant
        </button>
      </header>

      <section className="py-16 px-4 max-w-5xl mx-auto grid gap-12 md:grid-cols-3">
        <div>
          <h2 className="text-xl font-semibold mb-2">1. Create an Assistant</h2>
          <p>Register and launch your branded AI assistant in seconds — no technical setup needed.</p>
        </div>
        <div>
          <h2 className="text-xl font-semibold mb-2">2. Upload a Product PDF</h2>
          <p>Drop in your product manual or support doc. We’ll turn it into a structured flow.</p>
        </div>
        <div>
          <h2 className="text-xl font-semibold mb-2">3. Share & Chat</h2>
          <p>Send your customers a URL where they can chat with the assistant — text-only, for now.</p>
        </div>
      </section>

      <section className="bg-gray-100 py-16 px-4 text-center">
        <h2 className="text-3xl font-bold mb-4">Why Free for Early Adopters?</h2>
        <p className="max-w-2xl mx-auto text-lg mb-6">
          We’re building the future of AI support — and we need your help to shape it. Early adopters get permanent access to our <strong>text-only plan for free</strong>.
        </p>
        <ul className="grid gap-4 md:grid-cols-2 max-w-3xl mx-auto text-left">
          <li>✓ 1 customizable assistant</li>
          <li>✓ 3 products per assistant</li>
          <li>✓ Unlimited GPT-4o-mini text chats</li>
          <li>✓ Automatic flow generation from PDFs</li>
          <li>✓ Clean step-by-step interface</li>
          <li>✓ Email support</li>
        </ul>
      </section>

      <section className="py-16 px-4 max-w-4xl mx-auto text-center">
        <h2 className="text-3xl font-bold mb-6">Upgrade When You're Ready</h2>
        <div className="overflow-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-indigo-100">
                <th className="p-3">Feature</th>
                <th className="p-3">Free Text Plan</th>
                <th className="p-3">Coming Pro Plan</th>
              </tr>
            </thead>
            <tbody>
              <tr><td className="p-3">Assistants</td><td className="p-3">1</td><td className="p-3">3+</td></tr>
              <tr className="bg-gray-50"><td className="p-3">Products</td><td className="p-3">3</td><td className="p-3">10+</td></tr>
              <tr><td className="p-3">GPT-4o-mini</td><td className="p-3">Unlimited</td><td className="p-3">Unlimited</td></tr>
              <tr className="bg-gray-50"><td className="p-3">Audio / Voice Steps</td><td className="p-3">-</td><td className="p-3">Included</td></tr>
              <tr><td className="p-3">Image Step Support</td><td className="p-3">-</td><td className="p-3">Included</td></tr>
              <tr className="bg-gray-50"><td className="p-3">Branding</td><td className="p-3">Limited</td><td className="p-3">Full Custom</td></tr>
              <tr><td className="p-3">Analytics</td><td className="p-3">Basic</td><td className="p-3">Advanced</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <section className="bg-indigo-600 text-white text-center py-16 px-4">
        <h2 className="text-3xl font-bold mb-4">Join as an early adopter and launch your first assistant in minutes.</h2>
        <button onClick={() => navigate("/register")} className="mt-4 px-8 py-4 bg-white text-indigo-600 font-semibold rounded-2xl shadow-lg hover:shadow-2xl transition">
          Create My Free Assistant Now
        </button>
        <p className="mt-4 text-sm italic">*Spots are limited. This offer will not last forever.</p>
      </section>
    </div>
  );
}
