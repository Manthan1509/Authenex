import React, { useState } from 'react';
import AutheLogo from '../assets/logo.png';

// Simple i18n implementation
const translations = {
  en: {
    home: "Home",
    about: "About",
    verifier: "Verifier",
    institute: "Institute",
    support: "Support",
    services: "Services",
    contact: "Contact"
  }
};

const useTranslation = (lang = 'en') => {
  return translations[lang] || translations.en;
};

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const t = useTranslation();

//   for smooth about scrooling
const scrollToAbout = () => {
  const aboutSection = document.getElementById("about");
  if (aboutSection) {
    aboutSection.scrollIntoView({ behavior: "smooth" });
  }
};

  return (
    <nav className="bg-gray-800 text-white">
      <div className="max-w-[1390px] mx-auto px-4 pt-2 pb-2.5 sm:px-6 lg:px-1">
        <div className="flex justify-between h-16 items-center">
          {/* Logo */}
           <div className="flex items-center space-x-4">
            <img src={AutheLogo} alt="Logo" className="h-16 " />
            <span className="text-3xl font-bold">Authenex</span>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex space-x-13 text-[19px] font-bold">
            <a href="#home" className="hover:text-yellow-400">{t.home}</a>
            <a onClick={scrollToAbout} className="hover:text-yellow-400 cursor-pointer">{t.about}</a>
            <a href="#services" className="hover:text-yellow-400">{t.verifier}</a>
            <a href="#contact" className="hover:text-yellow-400">{t.institute}</a>
            <a href="#contact" className="hover:text-yellow-400">{t.support}</a>
          </div>

          {/* Mobile Hamburger */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="focus:outline-none"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                {isOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-gray-700 px-2 pt-2 pb-3 space-y-1">
          <a href="#home" className="block px-3 py-2 rounded hover:bg-gray-600">{t.home}</a>
          <a href="#about" className="block px-3 py-2 rounded hover:bg-gray-600">{t.about}</a>
          <a href="#services" className="block px-3 py-2 rounded hover:bg-gray-600">{t.services}</a>
          <a href="#contact" className="block px-3 py-2 rounded hover:bg-gray-600">{t.contact}</a>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
