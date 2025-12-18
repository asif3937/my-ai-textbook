import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Manual sidebar for the AI textbook structure
  textbookSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['intro'],
    },
    {
      type: 'category',
      label: 'Physical AI Fundamentals',
      items: ['physical-ai/intro', 'physical-ai/basics'],
    },
    {
      type: 'category',
      label: 'Humanoid Robotics',
      items: ['humanoid-robotics/intro', 'humanoid-robotics/basics'],
    },
    {
      type: 'category',
      label: 'ROS 2 Fundamentals',
      items: ['ros2/intro', 'ros2/basics', 'ros2/nodes-topics'],
    },
    {
      type: 'category',
      label: 'Digital Twin Simulation',
      items: ['digital-twin/intro', 'digital-twin/gazebo', 'digital-twin/isaac'],
    },
    {
      type: 'category',
      label: 'Vision-Language-Action Systems',
      items: ['vla/intro', 'vla/integration'],
    },
    {
      type: 'category',
      label: 'Capstone Project',
      items: ['capstone/intro', 'capstone/project'],
    },
  ],
};

export default sidebars;
