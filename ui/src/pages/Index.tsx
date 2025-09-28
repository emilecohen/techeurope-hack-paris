"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Navigation from "@/components/Navigation";

export default function HomePage() {
  const [form, setForm] = useState({
    companyName: "",
    rssLink: "",
    categories: "",
    language: "",
    maxArticles: 50,
    frequency: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (key: string, value: any) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const safeForm = {
      ...form,
      maxArticles: Math.min(Number(form.maxArticles), 200),
    };

    console.log(safeForm);

    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8080/posting", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(safeForm),
      });

      if (!response.ok) throw new Error(`Error: ${response.statusText}`);
      const data = await response.json();
      console.log("Server response:", data);
    } catch (error: any) {
      console.error(error);
      alert("Failed to submit form. Some network issue.");
    } finally {
      setLoading(false);
    }
  };

  const isFormValid =
    form.companyName.trim() !== "" &&
    form.rssLink.trim() !== "" &&
    form.language.trim() !== "" &&
    form.frequency.trim() !== "";

  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      {/* Video de fondo */}
      <video
        autoPlay
        muted
        loop
        playsInline
        className="absolute top-0 left-0 w-full h-full object-contain mx-auto my-auto z-0 bg-black"
      >
        <source src="/background.mp4" type="video/mp4" />
        Tu navegador no soporta video en HTML5.
      </video>

      <div className="absolute inset-0 bg-black/50 z-10"></div>

      {/* Contenido principal */}
      <div className="relative z-20 min-h-screen">
        <Navigation />
        <main className="min-h-screen flex items-center justify-center p-6">
          <Card className="w-full max-w-lg shadow-lg bg-white/80 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-xl font-semibold text-center">
                Newspaper Registration
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form className="space-y-6" onSubmit={handleSubmit}>
                {/* Company Name */}
                <div className="space-y-2">
                  <Label htmlFor="companyName">Company Name</Label>
                  <Input
                    id="companyName"
                    placeholder="e.g. The Daily Times"
                    value={form.companyName}
                    onChange={(e) => handleChange("companyName", e.target.value)}
                  />
                </div>

                {/* RSS Link */}
                <div className="space-y-2">
                  <Label htmlFor="rssLink">RSS Feed Link</Label>
                  <Input
                    id="rssLink"
                    placeholder="https://example.com/rss"
                    value={form.rssLink}
                    onChange={(e) => handleChange("rssLink", e.target.value)}
                  />
                </div>

                {/* Categories */}
                <div className="space-y-2">
                  <Label htmlFor="categories">Categories</Label>
                  <Textarea
                    id="categories"
                    placeholder="Politics, Sports, Technology"
                    value={form.categories}
                    onChange={(e) => handleChange("categories", e.target.value)}
                  />
                  <p className="text-sm text-muted-foreground">
                    Separate multiple categories with commas.
                  </p>
                </div>

                {/* Language + Max Articles + Frequency */}
                <div className="flex justify-between gap-4">
                  {/* Language */}
                  <div className="space-y-2 w-1/3">
                    <Label htmlFor="language">Language</Label>
                    <Select
                      value={form.language}
                      onValueChange={(val) => handleChange("language", val)}
                    >
                      <SelectTrigger id="language">
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent side="top">
                        <SelectItem value="en">English</SelectItem>
                        <SelectItem value="es">Spanish</SelectItem>
                        <SelectItem value="fr">French</SelectItem>
                        <SelectItem value="de">German</SelectItem>
                        <SelectItem value="it">Italian</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Max Retrieval Articles */}
                  <div className="w-24 space-y-2">
                    <Label htmlFor="maxArticles">Max Articles</Label>
                    <Input
                      id="maxArticles"
                      type="number"
                      min={1}
                      max={200}
                      value={form.maxArticles}
                      onChange={(e) => handleChange("maxArticles", Number(e.target.value))}
                    />
                  </div>

                  {/* Frequency */}
                  <div className="space-y-2 w-1/3">
                    <Label htmlFor="frequency">Frequency</Label>
                    <Select
                      value={form.frequency}
                      onValueChange={(val) => handleChange("frequency", val)}
                    >
                      <SelectTrigger id="frequency">
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="15m">Every 15 minutes</SelectItem>
                        <SelectItem value="30m">Every 30 minutes</SelectItem>
                        <SelectItem value="1h">Every hour</SelectItem>
                        <SelectItem value="6h">Every 6 hours</SelectItem>
                        <SelectItem value="12h">Every 12 hours</SelectItem>
                        <SelectItem value="24h">Daily</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                {/* Submit Button */}
                <Button
                  type="submit"
                  className="w-full cursor-pointer"
                  disabled={loading || !isFormValid}
                >
                  {loading ? "Submitting..." : "Submit"}
                </Button>
              </form>
            </CardContent>
          </Card>
        </main>
      </div>
    </div>
  );
}
