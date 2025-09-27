import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, BarChart3, Globe, Shield, Zap } from "lucide-react";
import { Link } from "react-router-dom";
import Navigation from "@/components/Navigation";
import heroImage from "@/assets/hero-video-bg.jpg";

const Index = () => {
  const features = [
    {
      icon: <Globe className="h-8 w-8" />,
      title: "Global News Sources",
      description: "Access news from trusted sources worldwide including The Washington Post, BBC, Reuters, and more."
    },
    {
      icon: <BarChart3 className="h-8 w-8" />,
      title: "Real-time Analytics",
      description: "Track and analyze news trends with our comprehensive dashboard and filtering tools."
    },
    {
      icon: <Zap className="h-8 w-8" />,
      title: "AI-Powered Agent",
      description: "Interact with our intelligent video agent for personalized news summaries and insights."
    },
    {
      icon: <Shield className="h-8 w-8" />,
      title: "Reliable Sources",
      description: "All news sources are verified and rated for reliability to ensure accurate information."
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center overflow-hidden">
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: `url(${heroImage})` }}
        >
          <div className="absolute inset-0 bg-hero/80"></div>
        </div>
        
        <div className="relative z-10 text-center text-hero-foreground px-6 max-w-4xl">
          <h1 className="text-6xl md:text-7xl font-bold mb-6 leading-tight">
            Your Gateway to 
            <span className="bg-gradient-to-r from-primary-glow to-white bg-clip-text text-transparent block">
              Global News
            </span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-hero-foreground/90 max-w-2xl mx-auto">
            Monitor, analyze, and interact with news from trusted sources worldwide through our AI-powered platform.
          </p>
          <Link to="/dashboard">
            <Button 
              size="lg" 
              className="bg-gradient-to-r from-primary to-primary-glow hover:shadow-[var(--shadow-elegant)] text-lg px-8 py-4 transition-all duration-300 transform hover:scale-105"
            >
              Try Now
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </div>
        
        {/* Floating Elements */}
        <div className="absolute top-20 left-20 w-20 h-20 bg-primary/20 rounded-full blur-xl"></div>
        <div className="absolute bottom-20 right-20 w-32 h-32 bg-primary-glow/20 rounded-full blur-xl"></div>
      </section>
      
      {/* Features Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Why Choose NewsHub?</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Comprehensive news monitoring with cutting-edge AI technology
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card 
                key={index} 
                className="shadow-[var(--shadow-card)] hover:shadow-[var(--shadow-elegant)] transition-all duration-300 transform hover:-translate-y-2 bg-gradient-to-br from-background to-secondary/20"
              >
                <CardHeader className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-br from-primary/10 to-primary-glow/10 rounded-full flex items-center justify-center mx-auto mb-4 text-primary">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-center">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-secondary/30 to-background">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Get Started?</h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join thousands of users who trust NewsHub for their daily news monitoring and analysis.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/dashboard">
              <Button 
                size="lg" 
                className="bg-gradient-to-r from-primary to-primary-glow hover:shadow-[var(--shadow-elegant)] transition-all duration-300"
              >
                View Dashboard
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link to="/agent">
              <Button 
                variant="outline" 
                size="lg"
                className="border-primary text-primary hover:bg-primary hover:text-primary-foreground transition-all duration-300"
              >
                Meet AI Agent
              </Button>
            </Link>
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="bg-hero text-hero-foreground py-12">
        <div className="container mx-auto px-6 text-center">
          <div className="font-bold text-2xl mb-4 bg-gradient-to-r from-primary-glow to-white bg-clip-text text-transparent">
            NewsHub
          </div>
          <p className="text-hero-foreground/70 mb-6">
            Your trusted source for global news monitoring and AI-powered insights.
          </p>
          <div className="flex justify-center gap-8 text-sm">
            <Link to="/" className="hover:text-primary-glow transition-colors">Home</Link>
            <Link to="/dashboard" className="hover:text-primary-glow transition-colors">Dashboard</Link>
            <Link to="/agent" className="hover:text-primary-glow transition-colors">Agent</Link>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;