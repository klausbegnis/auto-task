import './LandingPage.css';
import { useNavigate } from 'react-router-dom';

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      {/* Hero Section */}
      <section className="landing-hero">
        <div className="hero-content">
          <h1 className="hero-title">AI-Powered Development</h1>
          <p className="hero-subtitle">
            Automate your development workflow with AI that handles projects, issues, 
            and code reviews so you can focus on what matters.
          </p>
          <div className="hero-cta">
            <button className="btn btn-primary" onClick={() => navigate('/projects')}>Get Started</button>
            <button className="btn btn-outline">See How It Works</button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <h2 className="section-title">Automate Your Development Workflow</h2>
          <p className="section-subtitle">
            Our AI handles the repetitive tasks so you can focus on creative problem solving.
          </p>
          
          <div className="feature-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>AI Project Setup</h3>
              <p>
                Automatically scaffold new projects with best practices, 
                configured tooling, and optimized architecture.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🔍</div>
              <h3>Smart Issue Resolution</h3>
              <p>
                AI analyzes and fixes common bugs before they reach your queue, 
                with explanations for each change.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Automated Code Reviews</h3>
              <p>
                Continuous AI-powered code reviews that improve quality and 
                enforce standards without human bottlenecks.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Demo Section */}
      <section className="demo-section">
        <div className="container">
          <div className="demo-content">
            <div className="demo-text">
              <h2>See It In Action</h2>
              <p>
                Watch how our AI automatically converts GitHub issues into 
                working pull requests in minutes.
              </p>
              <ul className="demo-features">
                <li>Issue analysis and task breakdown</li>
                <li>Automatic code generation</li>
                <li>Test creation and validation</li>
                <li>Pull request with changelog</li>
              </ul>
            </div>
            <div className="demo-visual">
              <div className="code-window">
                <div className="window-header">
                  <div className="window-controls">
                    <span className="control red"></span>
                    <span className="control yellow"></span>
                    <span className="control green"></span>
                  </div>
                  <div className="window-title">issue-to-pr.ts</div>
                </div>
                <div className="code-content">
                  <pre>
                    {`// AI-generated solution for issue #42
function calculateDiscount(items) {
  return items.length > 5 ? 0.1 : 0;
}`}
                  </pre>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section
      <section className="cta-section">
        <div className="container">
          <h2>Ready to Automate Your Workflow?</h2>
          <p>
            Join thousands of developers who ship better code faster with AI assistance.
          </p>
          <button className="btn btn-primary btn-large">Start Free Trial</button>
          <p className="cta-note">No credit card required • 14-day trial</p>
        </div>
      </section> */}
    </div>
  );
}

export default LandingPage;