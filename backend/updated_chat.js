import React from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import AIChat from '../components/AIChat';
import './chat.module.css';

function ChatPage() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={`AI Chat - ${siteConfig.title}`}
      description="Interactive AI chatbot for the Physical AI textbook">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--12">
            <div className="text--center padding-horiz--md">
              <h1>AI Textbook Assistant</h1>
              <p>Ask questions about Physical AI, Humanoid Robotics, ROS 2, and more</p>
            </div>
            <AIChat />
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default ChatPage;