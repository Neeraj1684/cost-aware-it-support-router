"use client";

import { Activity, BrainCircuit, ShieldAlert, Wallet, LogOut, Send, CheckCircle, ChevronLeft, ChevronRight } from "lucide-react";
import { useSession, signOut } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect, useState, useCallback } from "react";

interface TicketLog {
  id: number;
  subject: string;
  body: string;
  engine: string;
  assigned_queue: string;
  confidence_score: number;
  latency_ms: number;
  status: string;
}

export default function Dashboard() {
  const { data: session, status } = useSession();
  const router = useRouter();
  
  const [tickets, setTickets] = useState<TicketLog[]>([]);
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // Pagination State
  const [page, setPage] = useState(1);
  const [totalTickets, setTotalTickets] = useState(0);
  const limit = 5; // Show 5 tickets per page

  // Security kick-out
  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/login");
    }
  }, [status, router]);

  const fetchTickets = useCallback(async () => {
    if (!session) return;
    try {
      const skip = (page - 1) * limit;
      const res = await fetch(`http://localhost:8000/api/v1/tickets/logs?skip=${skip}&limit=${limit}`, {
        headers: {
          "Authorization": `Bearer ${(session as any)?.accessToken}`
        }
      });
      
      // TOKEN EXPIRY HANDLING: If 60 mins passed, backend says 401. Kick them out.
      if (res.status === 401) {
        signOut();
        return;
      }

      if (res.ok) {
        const data = await res.json();
        setTickets(data.items);
        setTotalTickets(data.total);
      }
    } catch (error) {
      console.error("Failed to fetch tickets", error);
    }
  }, [session, page, limit]);

  useEffect(() => {
    if (status === "authenticated") fetchTickets();
  }, [status, fetchTickets]);

  const submitTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!subject || !body) return;
    
    setIsSubmitting(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/tickets/route", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${(session as any)?.accessToken}`
        },
        body: JSON.stringify({ subject, body }),
      });
      
      if (res.status === 401) return signOut();
      
      setSubject("");
      setBody("");
      setPage(1); // Jump back to page 1 to see the new ticket
      fetchTickets();
    } catch (error) {
      console.error("Error submitting ticket", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const resolveTicket = async (ticketId: number) => {
    try {
      const res = await fetch(`http://localhost:8000/api/v1/tickets/${ticketId}/status`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${(session as any)?.accessToken}`
        },
        body: JSON.stringify({ status: "resolved" }),
      });
      if (res.status === 401) return signOut();
      fetchTickets(); 
    } catch (error) {
      console.error("Error resolving ticket", error);
    }
  };

  if (status === "loading") return <div className="min-h-screen bg-gray-50 flex items-center justify-center">Loading...</div>;
  if (!session) return null;

  const isAdmin = session.user?.name === "luffy";
  const totalPages = Math.ceil(totalTickets / limit);

  return (
    <main className="min-h-screen bg-gray-50 p-8 text-gray-900">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-gray-900">
              IT Support Router
            </h1>
            <p className="text-gray-500 mt-2">
              Welcome back, <span className="font-semibold">{session.user?.name}</span>
              {isAdmin && <span className="ml-2 px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded-full font-bold">ADMIN</span>}
            </p>
          </div>
          <button 
            onClick={() => signOut()}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            <LogOut size={16} /> Sign Out
          </button>
        </div>

        {/* Dynamic Grid: Admins get 1 wide column, Users get the split view */}
        <div className={`grid grid-cols-1 ${!isAdmin ? 'lg:grid-cols-3' : ''} gap-8`}>
          
          {/* User Only: Ticket Submission Form */}
          {!isAdmin && (
            <div className="lg:col-span-1">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h2 className="text-lg font-semibold mb-4 text-gray-900">Submit New Ticket</h2>
                <form onSubmit={submitTicket} className="space-y-4">
                  <div>
                    <input
                      type="text"
                      placeholder="Ticket Subject"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-sm"
                      value={subject}
                      onChange={(e) => setSubject(e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <textarea
                      placeholder="Describe the technical issue in detail..."
                      rows={5}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-sm resize-none"
                      value={body}
                      onChange={(e) => setBody(e.target.value)}
                      required
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="w-full flex items-center justify-center gap-2 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
                  >
                    <Send size={16} />
                    {isSubmitting ? "Routing..." : "Route Ticket"}
                  </button>
                </form>
              </div>
            </div>
          )}

          {/* Ticket Feed & Metrics (Takes up remaining space) */}
          <div className={!isAdmin ? "lg:col-span-2" : "w-full"}>
            
            {/* Feed */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                <h3 className="text-sm font-semibold text-gray-900">
                  {isAdmin ? "Global Organization Feed" : "Your Tickets"}
                </h3>
                <span className="text-xs text-gray-500">Total: {totalTickets}</span>
              </div>
              
              <div className="divide-y divide-gray-100">
                {tickets.map((ticket) => (
                  <div key={ticket.id} className="px-6 py-4 flex items-center justify-between hover:bg-gray-50">
                    <div className="flex-1 pr-4">
                      <div className="flex items-center gap-3">
                        <p className="text-sm font-medium text-gray-900">{ticket.subject}</p>
                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                          ticket.status === 'resolved' ? 'bg-gray-100 text-gray-500' : 'bg-blue-100 text-blue-700'
                        }`}>
                          {ticket.status}
                        </span>
                      </div>
                      <p className="text-xs text-gray-500 mt-1 line-clamp-1">{ticket.body}</p>
                      <p className="text-xs text-gray-400 mt-2">Routed to: <span className="font-semibold text-gray-600">{ticket.assigned_queue}</span></p>
                    </div>
                    
                    <div className="flex flex-col items-end gap-2 shrink-0">
                      <span className={`px-2 py-1 rounded-md text-xs font-medium ${ticket.engine.includes("ML") ? "bg-green-100 text-green-700" : "bg-amber-100 text-amber-700"}`}>
                        {ticket.engine.split(' ')[0]}
                      </span>
                      
                      {isAdmin && ticket.status !== 'resolved' && (
                        <button 
                          onClick={() => resolveTicket(ticket.id)}
                          className="flex items-center gap-1 mt-1 text-xs font-semibold text-blue-600 hover:text-blue-800 transition-colors"
                        >
                          <CheckCircle size={14} /> Resolve
                        </button>
                      )}
                    </div>
                  </div>
                ))}
                {tickets.length === 0 && (
                  <div className="p-8 text-center text-sm text-gray-500">No tickets found.</div>
                )}
              </div>

              {/* Pagination Controls */}
              {totalPages > 1 && (
                <div className="px-6 py-4 border-t border-gray-100 flex items-center justify-between bg-gray-50">
                  <button 
                    onClick={() => setPage(p => Math.max(1, p - 1))}
                    disabled={page === 1}
                    className="flex items-center gap-1 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50"
                  >
                    <ChevronLeft size={16} /> Previous
                  </button>
                  <span className="text-sm text-gray-500">
                    Page {page} of {totalPages}
                  </span>
                  <button 
                    onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                    disabled={page === totalPages}
                    className="flex items-center gap-1 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50"
                  >
                    Next <ChevronRight size={16} />
                  </button>
                </div>
              )}
            </div>

          </div>
        </div>
      </div>
    </main>
  );
}