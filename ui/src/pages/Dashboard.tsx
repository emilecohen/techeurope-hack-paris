import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Search } from "lucide-react";
import Navigation from "@/components/Navigation";

const Dashboard = () => {
  const [searchTerm, setSearchTerm] = useState("");

  const newsSources = [
    {
      id: 1,
      name: "The Washington Post",
      category: "Politics",
      reliability: "High",
      subscribers: "2.8M",
      status: "Active",
      lastUpdated: "2 hours ago"
    },
    {
      id: 2,
      name: "BBC News",
      category: "World",
      reliability: "High",
      subscribers: "4.2M",
      status: "Active",
      lastUpdated: "1 hour ago"
    },
    {
      id: 3,
      name: "Reuters",
      category: "Business",
      reliability: "High",
      subscribers: "3.1M",
      status: "Active",
      lastUpdated: "30 minutes ago"
    },
    {
      id: 4,
      name: "CNN",
      category: "Breaking News",
      reliability: "Medium",
      subscribers: "5.7M",
      status: "Active",
      lastUpdated: "15 minutes ago"
    },
    {
      id: 5,
      name: "The Guardian",
      category: "Opinion",
      reliability: "High",
      subscribers: "1.9M",
      status: "Active",
      lastUpdated: "45 minutes ago"
    },
    {
      id: 6,
      name: "Associated Press",
      category: "General",
      reliability: "High",
      subscribers: "2.3M",
      status: "Active",
      lastUpdated: "1 hour ago"
    }
  ];

  const filteredSources = newsSources.filter(source =>
    source.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    source.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getReliabilityColor = (reliability: string) => {
    switch (reliability.toLowerCase()) {
      case 'high': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <div className="pt-24 pb-12">
        <div className="container mx-auto px-6">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-4">News Sources Dashboard</h1>
            <p className="text-muted-foreground text-lg">
              Monitor and manage your news information sources
            </p>
          </div>
          
          <Card className="shadow-[var(--shadow-card)]">
            <CardHeader className="bg-gradient-to-r from-secondary/50 to-background border-b">
              <div className="flex items-center justify-between">
                <CardTitle className="text-2xl">Active News Sources</CardTitle>
                <div className="relative w-80">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                  <Input
                    placeholder="Search sources..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-[hsl(var(--table-header))]">
                    <tr>
                      <th className="text-left py-4 px-6 font-semibold text-foreground/80">Source Name</th>
                      <th className="text-left py-4 px-6 font-semibold text-foreground/80">Category</th>
                      <th className="text-left py-4 px-6 font-semibold text-foreground/80">Reliability</th>
                      <th className="text-left py-4 px-6 font-semibold text-foreground/80">Subscribers</th>
                      <th className="text-left py-4 px-6 font-semibold text-foreground/80">Status</th>
                      <th className="text-left py-4 px-6 font-semibold text-foreground/80">Last Updated</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredSources.map((source, index) => (
                      <tr 
                        key={source.id} 
                        className={`border-b border-border hover:bg-secondary/30 transition-colors ${
                          index % 2 === 0 ? 'bg-background' : 'bg-secondary/20'
                        }`}
                      >
                        <td className="py-4 px-6 font-medium">{source.name}</td>
                        <td className="py-4 px-6">
                          <Badge variant="outline" className="bg-primary/10 text-primary border-primary/30">
                            {source.category}
                          </Badge>
                        </td>
                        <td className="py-4 px-6">
                          <Badge className={getReliabilityColor(source.reliability)}>
                            {source.reliability}
                          </Badge>
                        </td>
                        <td className="py-4 px-6 text-muted-foreground">{source.subscribers}</td>
                        <td className="py-4 px-6">
                          <Badge className="bg-green-100 text-green-800">
                            {source.status}
                          </Badge>
                        </td>
                        <td className="py-4 px-6 text-muted-foreground">{source.lastUpdated}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;