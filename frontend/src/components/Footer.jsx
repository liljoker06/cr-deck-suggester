import React from "react";

export default function Footer() {
  return (
    <div className="bg-gradient-to-r from-blue-900 via-purple-900 to-blue-800">
      <footer className="bg-gradient-to-r from-blue-900 via-purple-900 to-blue-800">
        <div className="container px-4 mx-auto">
          <div className="pt-6 pb-6 mx-auto max-w-4xl">
            <a className="block md:mx-auto mb-5 max-w-max" href="#">
              <a className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
                <img src="/CR-Logo.png" alt="Clash Royale Logo" className="h-10 w-auto" />
                <span className="text-xl font-bold text-yellow-400 hidden sm:block">Mousieur DeckSVP</span>
              </a>
            </a>
            <div className="flex flex-wrap justify-center -mx-3 lg:-mx-6">
              <div className="w-full md:w-auto p-3 md:px-6">
                <a
                  href="/#"
                  className="inline-block text-lg text-white hover:text-yellow-400 font-medium transition-colors"
                >
                  Terms
                </a>
              </div>
              <div className="w-full md:w-auto p-3 md:px-6">
                <a
                  href="/#"
                  className="inline-block text-lg text-white hover:text-yellow-400 font-medium transition-colors"
                >
                  Privacy
                </a>
              </div>
              <div className="w-full md:w-auto p-3 md:px-6">
                <a
                  className="inline-block text-lg text-white hover:text-yellow-400 font-medium transition-colors"
                  href="/#"
                >
                  Contact Us
                </a>
              </div>
              <div className="w-full md:w-auto p-3 md:px-6">
                <a
                  href="/#"
                  className="inline-block text-lg text-white hover:text-yellow-400 font-medium transition-colors"
                >
                  Careers
                </a>
              </div>
            </div>
          </div>
        </div>
        <div className="border-b border-gray-700"></div>
        <div className="container px-4 mx-auto">
          <p className="py-4 md:pb-6 text-md text-gray-300 font-medium text-center">
            © 2025 MousieurDeckSVP.com. Tout droit réservé.
          </p>
        </div>
      </footer>
    </div>
  );
}
