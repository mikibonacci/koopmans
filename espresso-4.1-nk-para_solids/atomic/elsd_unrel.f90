!
! Copyright (C) 2004-2007 QUANTUM-Espresso group
! This file is distributed under the terms of the
! GNU General Public License. See the file `License'
! in the root directory of the present distribution,
! or http://www.gnu.org/copyleft/gpl.txt .
!
!
!---------------------------------------------------------------
subroutine elsd_unrel (zed,grid,rho,vxt,vh,vxc,exc,excgga,nwf,nspin,enl,oc,   &
                 etot,ekin,encl,ehrt,ecxc,evxt,ekinnl)    
  !---------------------------------------------------------------
  !
  !   atomic total energy in the local-spin-density scheme
  !   atomic pseudopotentials with nonlinear core correction are allowed
  !   gradient correction allowed (A. Dal Corso fecit AD 1993)
  !
  use kinds, only : DP
  use radial_grids, only: ndmx, radial_grid_type
  use funct, only: get_iexch
  use ld1inc, only: vx
  implicit none
  integer, intent(in) :: nwf, nspin
  type(radial_grid_type),intent(in)::grid
  real(DP), intent(in)  :: zed
  real(DP), intent(in)  :: enl(nwf), oc(nwf), rho(ndmx,2), &
                           vxt(ndmx), vh(ndmx), vxc(ndmx,2), exc(ndmx), &
                           excgga(ndmx), ekinnl(nwf)
  real(DP), intent(out) :: etot,encl,ekin,ehrt,ecxc,evxt
  real(DP),allocatable :: f1(:), f2(:), f3(:), f4(:), f5(:)
  real(DP) :: int_0_inf_dr, rhotot
  integer:: i,n,is,ierr
  logical:: oep

  oep=get_iexch().eq.4

  allocate(f1(grid%mesh),stat=ierr)
  allocate(f2(grid%mesh),stat=ierr)
  allocate(f3(grid%mesh),stat=ierr)
  allocate(f4(grid%mesh),stat=ierr)
  allocate(f5(grid%mesh),stat=ierr)

  do i=1,grid%mesh
     rhotot=rho(i,1)
     if (nspin==2) rhotot=rhotot+rho(i,2) 
!
!   The integral for the energy due to the interaction with nuclei
!
     f1(i)=-2.0_DP*zed/grid%r(i) * rhotot
!
!   The integral for the Hartree energy
!
     f2(i)= vh (i) * rhotot
!
!   The integral for the exchange and correlation energy 
!
     f3(i) = exc(i) * rhotot + excgga(i)
!
!   The integral for the interaction with an external potential
!
     f4(i)= vxt(i) * rhotot
!
!   The integral to be subtracted to the sum of the eigenvalues to
!   get the kinetic energy
!
     f5(i) =-vxc(i,1)*rho(i,1)-f1(i)-f2(i)-f4(i)
     if (nspin==2) f5(i) =f5(i)-vxc(i,2)*rho(i,2)

     if (oep) then
        do is = 1, nspin
           f5(i) = f5(i) - vx(i,is)*rho(i,is)
        end do
     end if
  enddo
!
!  Now compute the integrals
!
  encl=       int_0_inf_dr(f1,grid,grid%mesh,1)
  ehrt=0.5_DP*int_0_inf_dr(f2,grid,grid%mesh,2)
  ecxc=       int_0_inf_dr(f3,grid,grid%mesh,2)
  evxt=       int_0_inf_dr(f4,grid,grid%mesh,2)
!
!  The kinetic energy is the sum of the eigenvalues plus the f5 integral
!
  ekin = 0.0_dp
  do n=1,nwf
     ekin=ekin+oc(n)*ekinnl(n)
  enddo

  if (oep) call add_exchange (ecxc)

  etot= ekin + encl + ehrt + ecxc + evxt

  deallocate(f5)
  deallocate(f4)
  deallocate(f3)
  deallocate(f2)
  deallocate(f1)

  return
end subroutine elsd_unrel