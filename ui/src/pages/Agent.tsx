import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Play, Mic, MicOff, Video, VideoOff } from "lucide-react";
import { useState } from "react";
import Navigation from "@/components/Navigation";

const Agent = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isVideoOn, setIsVideoOn] = useState(true);

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <div className="pt-24 pb-12">
        <div className="container mx-auto px-6">
          <div className="mb-8 text-center">
            <h1 className="text-4xl font-bold mb-4">AI Video Agent</h1>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Interact with our AI-powered video agent to get personalized news summaries and insights
            </p>
          </div>
          
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Video Agent Area */}
            <div className="lg:col-span-2">
              <Card className="shadow-[var(--shadow-card)]">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Video className="h-5 w-5 text-primary" />
                    Video Agent
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="aspect-video bg-gradient-to-br from-hero to-hero/80 rounded-lg flex items-center justify-center mb-6 relative overflow-hidden">
                    <div className="absolute inset-0 bg-black/20"></div>
                    <div className="relative z-10 text-center text-white">
                      <div className="w-24 h-24 bg-white/20 rounded-full flex items-center justify-center mb-4 mx-auto backdrop-blur-sm">
                        <Play className="h-12 w-12 ml-1" />
                      </div>
                      <h3 className="text-xl font-semibold mb-2">AI Agent Ready</h3>
                      <p className="text-white/80">Click to start conversation</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-center gap-4">
                    <Button
                      variant={isRecording ? "destructive" : "default"}
                      size="lg"
                      onClick={() => setIsRecording(!isRecording)}
                      className="flex items-center gap-2"
                    >
                      {isRecording ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                      {isRecording ? "Stop Recording" : "Start Recording"}
                    </Button>
                    
                    <Button
                      variant="outline"
                      size="lg"
                      onClick={() => setIsVideoOn(!isVideoOn)}
                      className="flex items-center gap-2"
                    >
                      {isVideoOn ? <VideoOff className="h-4 w-4" /> : <Video className="h-4 w-4" />}
                      {isVideoOn ? "Turn Off Video" : "Turn On Video"}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
            
            {/* Controls and Features */}
            <div className="space-y-6">
              <Card className="shadow-[var(--shadow-card)]">
                <CardHeader>
                  <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button className="w-full justify-start" variant="outline">
                    <Play className="h-4 w-4 mr-2" />
                    Daily News Summary
                  </Button>
                  <Button className="w-full justify-start" variant="outline">
                    <Play className="h-4 w-4 mr-2" />
                    Breaking News Updates
                  </Button>
                  <Button className="w-full justify-start" variant="outline">
                    <Play className="h-4 w-4 mr-2" />
                    Market Analysis
                  </Button>
                  <Button className="w-full justify-start" variant="outline">
                    <Play className="h-4 w-4 mr-2" />
                    Weather & Sports
                  </Button>
                </CardContent>
              </Card>
              
              <Card className="shadow-[var(--shadow-card)]">
                <CardHeader>
                  <CardTitle>Agent Features</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3 text-sm text-muted-foreground">
                    <li className="flex items-start gap-2">
                      <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                      Real-time news analysis and summarization
                    </li>
                    <li className="flex items-start gap-2">
                      <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                      Interactive Q&A about current events
                    </li>
                    <li className="flex items-start gap-2">
                      <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                      Personalized content recommendations
                    </li>
                    <li className="flex items-start gap-2">
                      <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                      Multi-language support
                    </li>
                    <li className="flex items-start gap-2">
                      <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                      Voice and text interaction
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Agent;