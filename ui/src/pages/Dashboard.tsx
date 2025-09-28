import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Search } from "lucide-react";
import Navigation from "@/components/Navigation";
import articles from "./all_articles.json";

const Dashboard = () => {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredArticles = articles.filter(article =>
    article.media_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    article.language.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getLanguageBadgeColor = (lang: string) => {
    if (lang.startsWith("en")) return "bg-blue-100 text-blue-800";
    if (lang.startsWith("es")) return "bg-green-100 text-green-800";
    return "bg-gray-100 text-gray-800";
  };

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="pt-24 pb-12">
        <div className="container mx-auto px-6">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-4">Articles Dashboard</h1>
            <p className="text-muted-foreground text-lg">
              View and manage all articles from different sources
            </p>
          </div>

          <Card className="shadow-[var(--shadow-card)]">
            <CardHeader className="bg-gradient-to-r from-secondary/50 to-background border-b">
              <div className="flex items-center justify-between">
                <CardTitle className="text-2xl">Articles</CardTitle>
                <div className="relative w-80">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                  <Input
                    placeholder="Search articles..."
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
                      <th className="text-left py-4 px-6 font-semibold text-foreground/80">Source</th>
                      <th className="text-left py-4 px-6 font-semibold text-foreground/80">Title</th>
                      <th className="text-left py-4 px-6 font-semibold text-foreground/80">Language</th>
                      <th className="text-left py-4 px-6 font-semibold text-foreground/80">Date</th>
                      <th className="text-left py-4 px-6 font-semibold text-foreground/80">Link</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredArticles.map((article, index) => (
                      <tr
                        key={index}
                        className={`border-b border-border hover:bg-secondary/30 transition-colors ${
                          index % 2 === 0 ? "bg-background" : "bg-secondary/20"
                        }`}
                      >
                        <td className="py-4 px-6 font-medium">{article.media_name}</td>
                        <td className="py-4 px-6 max-w-xs truncate">{article.title}</td>
                        <td className="py-4 px-6">
                          <Badge className={getLanguageBadgeColor(article.language)}>
                            {article.language}
                          </Badge>
                        </td>
                        <td className="py-4 px-6 text-muted-foreground">
                          {new Date(article.date).toLocaleString()}
                        </td>
                        <td className="py-4 px-6">
                          <a
                            href={article.newspaper_link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-primary hover:underline"
                          >
                            View Article
                          </a>
                        </td>
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