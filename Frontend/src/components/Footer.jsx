import React from "react";
import { FaFacebookF, FaTwitter, FaLinkedinIn, FaInstagram } from "react-icons/fa";

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-14 rounded-t-2xl">
      <div className="max-w-7xl mx-auto px-6 md:px-12 lg:px-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 items-start">

          {/* Left Section - Logo & About */}
          <div className="flex flex-col">
            <div className="flex items-center space-x-2">
              <span className="text-3xl font-bold">⚡</span>
              <h1 className="text-3xl font-semibold">Authenex</h1>
            </div>
            <p className="mt-5 text-gray-400 text-base leading-relaxed">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit,
              sed do eiusmod tempor incididunt ut labore et dolore.
            </p>
          </div>

          {/* Middle Section - Navigation */}
          <div>
            <h2 className="text-xl font-semibold mb-5">Quick Links</h2>
            <ul className="flex flex-col space-y-3 text-gray-300 text-base">
              <li><a href="#" className="hover:text-white transition">Home</a></li>
              <li><a href="#" className="hover:text-white transition">About</a></li>
              <li><a href="#" className="hover:text-white transition">Courses</a></li>
              <li><a href="#" className="hover:text-white transition">Contact</a></li>
            </ul>
          </div>

          {/* Right Section - Social & Subscribe */}
          <div>
            <h2 className="text-xl font-semibold mb-5">Follow Us</h2>
            <div className="flex space-x-4 mb-5">
              <a href="#" className="text-2xl text-gray-400 hover:text-blue-500 transition"><FaFacebookF /></a>
              <a href="#" className="text-2xl text-gray-400 hover:text-sky-400 transition"><FaTwitter /></a>
              <a href="#" className="text-2xl text-gray-400 hover:text-blue-400 transition"><FaLinkedinIn /></a>
              <a href="#" className="text-2xl text-gray-400 hover:text-pink-400 transition"><FaInstagram /></a>
            </div>
            <button className="bg-white text-gray-900 font-semibold px-6 py-3 rounded-lg shadow hover:bg-gray-200 transition">
              Subscribe Now
            </button>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 border-t border-gray-700 pt-4 text-center text-gray-400 text-sm">
          © 2024 Authenex. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;