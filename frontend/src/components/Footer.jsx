import React from "react";

export default function Footer() {
  return (
    <div>
      <footer class="bg-gradient-to-r from-blue-900 via-purple-900 to-blue-800">
        <div class="container px-4 mx-auto">
          <div class="pt-6 pb-6 mx-auto max-w-4xl">
            <a class="block md:mx-auto mb-5 max-w-max" href="#">
              <a className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
                <img src="/CR-Logo.png" alt="Clash Royale Logo" className="h-10 w-auto" />
                <span className="text-xl font-bold text-yellow-400 hidden sm:block">Clash Royale</span>
              </a>
            </a>
            <div class="flex flex-wrap justify-center -mx-3 lg:-mx-6">
              <div class="w-full md:w-auto p-3 md:px-6">
                <a
                  href="/terms"
                  class="inline-block text-lg text-white hover:text-yellow-400 font-medium transition-colors"
                >
                  Terms
                </a>
              </div>
              <div class="w-full md:w-auto p-3 md:px-6">
                <a
                  href="/privacy"
                  class="inline-block text-lg text-white hover:text-yellow-400 font-medium transition-colors"
                >
                  Privacy
                </a>
              </div>
              <div class="w-full md:w-auto p-3 md:px-6">
                <a
                  class="inline-block text-lg text-white hover:text-yellow-400 font-medium transition-colors"
                  href=""
                >
                  Contact Us
                </a>
              </div>
              <div class="w-full md:w-auto p-3 md:px-6">
                <a
                  href="/careers"
                  class="inline-block text-lg text-white hover:text-yellow-400 font-medium transition-colors"
                >
                  Careers
                </a>
              </div>
            </div>
          </div>
        </div>
        <div class="border-b border-gray-700"></div>
        <div class="container px-4 mx-auto">
          <p class="py-4 md:pb-6 text-md text-gray-300 font-medium text-center">
            © 2025 CRSuggests.com. Tout droit réservé.
          </p>
        </div>
      </footer>
    </div>
  );
}
