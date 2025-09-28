import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const Navigation = () => {
  const location = useLocation();
  
  const navItems = [
    { path: "/", label: "Home" },
    { path: "/dashboard", label: "Dashboard" },
    { path: "/agent", label: "Agent" },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="font-bold text-2xl bg-gradient-to-r from-primary to-primary-glow bg-clip-text text-transparent">
            NewsCaster AI
          </div>
          
          <div className="flex items-center gap-8">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  "text-foreground/70 hover:text-foreground transition-colors duration-200 font-medium",
                  location.pathname === item.path && "text-primary"
                )}
              >
                {item.label}
              </Link>
            ))}
            
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;