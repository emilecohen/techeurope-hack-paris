import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Search, Edit, Save, X } from 'lucide-react';
import Navigation from '@/components/Navigation';
import articles from './all_articles.json';

const Dashboard = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [isEditingInstructions, setIsEditingInstructions] = useState(false);
  const [instructions, setInstructions] =
    useState(`You are BBC News, the world’s leading public service broadcaster. “Inform, educate, entertain.” Established 1922.

IDENTITY: We are the trusted voice at the heart of UK and global communities, acting in the public interest with independence and impartiality. Our personality is authoritative yet accessible, reflecting a commitment to serve all audiences through high-quality, distinctive output. We champion freedom of expression and uphold editorial integrity.

VOICE: Speak in a balanced, refined, and direct manner. We address our readers with clarity, context, and respect—always using “we” for the BBC and “our” for the community.

STYLE EXAMPLES:

“No noise. No agenda. Just expert analysis of the issues that matter most.”

“We take time and care to ensure the accuracy and impartiality of our news.”

“Distinctive, world-class programmes and journalism you can trust.”

CONTENT FOCUS: Prioritize news, sport, business, innovation, culture, arts, travel, earth, and science. Always provide accurate, impartial coverage and in-depth analysis. Strive to inform, educate, and entertain every audience, spotlighting diverse voices and underrepresented topics.

INTERACTION: Greet with “Welcome to BBC News.” When discussing stories, present verified facts with context and invite further questions by saying “Would you like to explore the story in greater depth?”

LOCAL KNOWLEDGE: Reference UK landmarks (e.g., London, Marconi studio, Strand) and global coverage. Know the BBC’s heritage in shaping media, local impact, and commitment to innovation.

Remember: You’re not a bot but BBC News itself—connecting people to trusted information and insight every day.`);
  const [tempInstructions, setTempInstructions] = useState(instructions);
  const [agentLanguage, setAgentLanguage] = useState('en');

  const filteredArticles = articles.filter(
    (article) =>
      article.media_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      article.language.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getLanguageBadgeColor = (lang: string) => {
    if (lang.startsWith('en')) return 'bg-blue-100 text-blue-800';
    if (lang.startsWith('es')) return 'bg-green-100 text-green-800';
    return 'bg-gray-100 text-gray-800';
  };

  const handleSaveInstructions = () => {
    setInstructions(tempInstructions);
    setIsEditingInstructions(false);
  };

  const handleCancelEdit = () => {
    setTempInstructions(instructions);
    setIsEditingInstructions(false);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="pt-24 pb-12">
        <div className="container mx-auto px-6">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-4">Dashboard</h1>
            <p className="text-muted-foreground text-lg">
              Manage your agent configuration and view articles
            </p>
          </div>

          <Tabs defaultValue="config" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="config">Agent Config</TabsTrigger>
              <TabsTrigger value="articles">Articles</TabsTrigger>
            </TabsList>

            <TabsContent value="config" className="mt-6">
              <Card className="shadow-[var(--shadow-card)]">
                <CardHeader className="bg-gradient-to-r from-secondary/50 to-background border-b">
                  <CardTitle className="text-2xl">
                    Agent Configuration
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-6">
                  <Tabs defaultValue="instructions" className="w-full">
                    <TabsList className="grid w-full grid-cols-2">
                      <TabsTrigger value="instructions">
                        Instructions & Language
                      </TabsTrigger>
                      <TabsTrigger value="mcp">MCP Config</TabsTrigger>
                    </TabsList>

                    <TabsContent
                      value="instructions"
                      className="mt-6 space-y-6">
                      {/* Instructions Section */}
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <Label className="text-lg font-semibold">
                            Instructions
                          </Label>
                          {!isEditingInstructions ? (
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => setIsEditingInstructions(true)}>
                              <Edit className="h-4 w-4 mr-2" />
                              Edit
                            </Button>
                          ) : (
                            <div className="flex gap-2">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={handleSaveInstructions}>
                                <Save className="h-4 w-4 mr-2" />
                                Save
                              </Button>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={handleCancelEdit}>
                                <X className="h-4 w-4 mr-2" />
                                Cancel
                              </Button>
                            </div>
                          )}
                        </div>

                        {isEditingInstructions ? (
                          <Textarea
                            value={tempInstructions}
                            onChange={(e) =>
                              setTempInstructions(e.target.value)
                            }
                            rows={20}
                            className="font-mono text-sm"
                            placeholder="Enter agent instructions..."
                          />
                        ) : (
                          <div className="bg-secondary/20 p-4 rounded-md border">
                            <pre className="text-sm whitespace-pre-wrap font-mono">
                              {instructions}
                            </pre>
                          </div>
                        )}
                      </div>

                      {/* Language Section */}
                      <div className="space-y-3">
                        <Label className="text-lg font-semibold">
                          Language
                        </Label>
                        <Select
                          value={agentLanguage}
                          onValueChange={setAgentLanguage}>
                          <SelectTrigger className="w-full max-w-sm">
                            <SelectValue placeholder="Select language" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="en">English</SelectItem>
                            <SelectItem value="es">Spanish</SelectItem>
                            <SelectItem value="fr">French</SelectItem>
                            <SelectItem value="de">German</SelectItem>
                            <SelectItem value="it">Italian</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </TabsContent>

                    <TabsContent value="mcp" className="mt-6">
                      <div className="space-y-6">
                        <div>
                          <h3 className="text-xl font-semibold mb-4">
                            Installation Guide
                          </h3>
                          <p className="text-muted-foreground mb-6">
                            Choose your preferred MCP client to see installation
                            instructions
                          </p>
                        </div>

                        <Tabs defaultValue="cursor" className="w-full">
                          <TabsList className="grid w-full grid-cols-4">
                            <TabsTrigger value="cursor">Cursor</TabsTrigger>
                            <TabsTrigger value="claude-teams">
                              Claude Teams
                            </TabsTrigger>
                            <TabsTrigger value="claude-desktop">
                              Claude Desktop
                            </TabsTrigger>
                            <TabsTrigger value="chatgpt">
                              OpenAI ChatGPT
                            </TabsTrigger>
                          </TabsList>

                          <TabsContent value="cursor" className="mt-6">
                            <div className="space-y-4">
                              <h4 className="text-lg font-semibold">
                                Install in Cursor
                              </h4>

                              <div className="space-y-3">
                                <p className="font-medium">
                                  One-click installation:
                                </p>
                                <Button className="w-full max-w-sm">
                                  Add to Cursor
                                </Button>
                              </div>

                              <div className="space-y-3">
                                <p className="font-medium">Manual steps:</p>
                                <ol className="list-decimal list-inside space-y-2 text-sm">
                                  <li>
                                    Go to Settings {'->'} Cursor Settings {'->'}{' '}
                                    Tools & Integrations
                                  </li>
                                  <li>Under MCP tools, click Add Custom MCP</li>
                                  <li>
                                    Paste the configuration below into mcp.json
                                  </li>
                                  <li>
                                    Save the file to apply the configuration
                                  </li>
                                  <li>Restart Cursor if prompted</li>
                                </ol>
                              </div>

                              <div className="space-y-2">
                                <p className="font-medium">Configuration:</p>
                                <div className="bg-secondary/20 p-4 rounded-md border">
                                  <pre className="text-sm font-mono">{`{
  "mcpServers": {
    "bbc-newspaper-agent": {
      "url": "https://techeurope-hack-pari-6f861422.alpic.live/mcp"
    }
  }
}`}</pre>
                                </div>
                              </div>
                            </div>
                          </TabsContent>

                          <TabsContent value="claude-teams" className="mt-6">
                            <div className="space-y-4">
                              <h4 className="text-lg font-semibold">
                                Install in Claude Teams
                              </h4>

                              <div className="space-y-3">
                                <p className="font-medium">Manual steps:</p>
                                <div className="bg-yellow-50 border border-yellow-200 p-3 rounded-md">
                                  <p className="text-sm font-medium text-yellow-800">
                                    Note: Only workspace owners and admins have
                                    permission to add custom connectors
                                  </p>
                                </div>
                                <ol className="list-decimal list-inside space-y-2 text-sm">
                                  <li>
                                    Navigate to Settings {'->'} Connectors
                                  </li>
                                  <li>
                                    Toggle to Organization connectors at the top
                                    of the page
                                  </li>
                                  <li>
                                    At the bottom of the page, click on Add
                                    custom connector and fill the following
                                    information:
                                  </li>
                                </ol>
                              </div>

                              <div className="space-y-3 bg-secondary/20 p-4 rounded-md border">
                                <div>
                                  <p className="font-medium">Name:</p>
                                  <code className="text-sm">
                                    bbc-newspaper-agent
                                  </code>
                                </div>
                                <div>
                                  <p className="font-medium">
                                    Remote MCP server URL:
                                  </p>
                                  <code className="text-sm">
                                    https://techeurope-hack-pari-6f861422.alpic.live/mcp
                                  </code>
                                </div>
                              </div>

                              <p className="text-sm">
                                Click Add to finish the setup
                              </p>
                            </div>
                          </TabsContent>

                          <TabsContent value="claude-desktop" className="mt-6">
                            <div className="space-y-4">
                              <h4 className="text-lg font-semibold">
                                Install in Claude Desktop
                              </h4>

                              <div className="space-y-4">
                                <div>
                                  <p className="font-medium mb-2">
                                    1. Make sure Node.js is installed
                                  </p>
                                  <p className="text-sm mb-2">
                                    In your terminal, check if Node.js is
                                    installed on your system by running:
                                  </p>
                                  <div className="bg-secondary/20 p-2 rounded border">
                                    <code className="text-sm">node -v</code>
                                  </div>
                                  <p className="text-sm mt-2">
                                    If Node.js isn't installed, download it from
                                    nodejs.org.
                                  </p>
                                </div>

                                <div>
                                  <p className="font-medium mb-2">
                                    2. Configure Claude Desktop
                                  </p>
                                  <ol className="list-decimal list-inside space-y-1 text-sm">
                                    <li>Go to Settings {'->'} Developer</li>
                                    <li>
                                      Click Edit config to open the
                                      claude_desktop_config.json file
                                    </li>
                                    <li>
                                      Add the MCP server configuration to the
                                      mcpServers section
                                    </li>
                                    <li>Paste the configuration below</li>
                                    <li>
                                      Save the file to apply the configuration
                                    </li>
                                    <li>Restart Claude Desktop</li>
                                  </ol>
                                </div>

                                <div className="space-y-2">
                                  <p className="font-medium">Configuration:</p>
                                  <div className="bg-secondary/20 p-4 rounded-md border">
                                    <pre className="text-sm font-mono">{`{
  "mcpServers": {
    "bbc-newspaper-agent": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://techeurope-hack-pari-6f861422.alpic.live/mcp"
      ]
    }
  }
}`}</pre>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </TabsContent>

                          <TabsContent value="chatgpt" className="mt-6">
                            <div className="space-y-4">
                              <h4 className="text-lg font-semibold">
                                Install in OpenAI ChatGPT
                              </h4>

                              <div className="bg-red-50 border border-red-200 p-3 rounded-md">
                                <p className="text-sm font-medium text-red-800">
                                  IMPORTANT: For now MCP servers are only
                                  supported in ChatGPT Plus and Pro versions
                                </p>
                              </div>

                              <div className="space-y-3">
                                <ol className="list-decimal list-inside space-y-2 text-sm">
                                  <li>
                                    Navigate to Settings {'->'} Connectors
                                  </li>
                                  <li>
                                    Scroll down and click on Advanced Settings
                                  </li>
                                  <li>Enable Developer mode</li>
                                  <li>
                                    Go back to the Settings {'->'} Connectors
                                    page, and click on Create in the Browser
                                    Connectors section
                                  </li>
                                  <li>
                                    You can now add a custom connector with the
                                    server URL:{' '}
                                    <code>
                                      https://techeurope-hack-pari-6f861422.alpic.live/mcp
                                    </code>
                                  </li>
                                  <li>
                                    In the Description field, add the server
                                    description:
                                  </li>
                                </ol>
                              </div>

                              <div className="bg-secondary/20 p-3 rounded-md border">
                                <p className="text-sm italic">
                                  This is the BBC Newspaper Agent MCP server.
                                  Access and analyze news articles directly from
                                  your favorite AI assistant!
                                </p>
                              </div>

                              <p className="text-sm">
                                Click on Create to add the MCP server as a
                                Connector. Now, to use the connector in a new
                                chat, just click on + {'->'} More and enable the
                                Developer mode. This will create a new tab in
                                the chat bar called Add Sources where you now
                                should see our MCP server listed.
                              </p>
                            </div>
                          </TabsContent>
                        </Tabs>
                      </div>
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="articles" className="mt-6">
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
                  <div className="overflow-x-auto max-h-[600px] overflow-y-auto">
                    <table className="w-full">
                      <thead className="bg-[hsl(var(--table-header))] sticky top-0">
                        <tr>
                          <th className="text-left py-4 px-6 font-semibold text-foreground/80">
                            Source
                          </th>
                          <th className="text-left py-4 px-6 font-semibold text-foreground/80">
                            Title
                          </th>
                          <th className="text-left py-4 px-6 font-semibold text-foreground/80">
                            Language
                          </th>
                          <th className="text-left py-4 px-6 font-semibold text-foreground/80">
                            Date
                          </th>
                          <th className="text-left py-4 px-6 font-semibold text-foreground/80">
                            Link
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {filteredArticles.map((article, index) => (
                          <tr
                            key={index}
                            className={`border-b border-border hover:bg-secondary/30 transition-colors ${
                              index % 2 === 0
                                ? 'bg-background'
                                : 'bg-secondary/20'
                            }`}>
                            <td className="py-4 px-6 font-medium">
                              {article.media_name}
                            </td>
                            <td className="py-4 px-6 max-w-xs truncate">
                              {article.title}
                            </td>
                            <td className="py-4 px-6">
                              <Badge
                                className={getLanguageBadgeColor(
                                  article.language
                                )}>
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
                                className="text-primary hover:underline">
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
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
