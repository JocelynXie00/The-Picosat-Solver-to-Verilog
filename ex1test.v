`timescale 1 ns / 1 ps
module test;
   reg clock,A;
   wire Y;
   ex1 x(clock,A,Y);
   initial begin
      {x.S1,x.S0,A} = 0;
      clock = 0;
   end

   always #0.5 clock=~clock;

   always @(posedge clock) begin 
      if ({x.S1,x.S0} == 2'b11) begin
         $display("%8d",$time," reached target");
         $finish;
      end
      A = $random;
      if ($time > 100000) begin
         $display("time out");
         $finish;
      end
   end

endmodule

module ex1(clock,A,Y);
input clock;
input A;
output Y;
reg S0,S1;
wire X1,NS0,NS1;
and g0(X1,S0,S1);
and g1(NS1,A,X1);
not g2(NS0,X1);
and g3(Y,A,X1);
always @(posedge clock) begin
S1<=NS1;
S0<=NS0;
end
endmodule
